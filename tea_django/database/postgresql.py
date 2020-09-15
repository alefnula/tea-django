import os
import shutil
import socket
from pathlib import Path
from datetime import datetime
from typing import Optional, Union, List

from django.conf import settings
from tea.process import execute
from tea_django.errors import DatabaseError


class PostgreSQLError(DatabaseError):
    def __init__(
        self,
        command: str,
        exit_code: int,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ):
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

        message = f"{command} failed: {exit_code}"
        if stdout:
            message += f"\n\nStdout\n------\n{stdout}"
        if stderr:
            message += f"\n\nStderr\n------\n{stderr}"

        super().__init__(message=message)


class PostgreSQL:
    """Class for manipulating PostgreSQL database."""

    DB_DUMP_CREATE = [
        "DROP DATABASE IF EXISTS {database}",
        "CREATE DATABASE {database}",
        "GRANT ALL PRIVILEGES ON DATABASE {database} TO {user}",
    ]

    def __init__(self):
        # Database parameters
        db = settings.DATABASES["default"]
        self.host = db["HOST"]
        self.port = db["PORT"]
        self.user = db["USER"]
        self.database = db["NAME"]
        self.password = db["PASSWORD"]

        self.db_params = ["-h", self.host, "-p", self.port, "-U", self.user]
        self.env = {"PGPASSWORD": self.password}

    def run(self, command: str, arguments: Optional[Union[str, List[str]]]):
        exe = shutil.which(command)
        if exe is None:
            raise DatabaseError(message=f"`{command}` command is not found.")

        if arguments is None:
            command = [exe]
        elif not isinstance(arguments, (list, tuple)):
            command = [exe, str(arguments)]
        else:
            command = [exe, *[str(arg) for arg in arguments]]
        exit_code, stdout, stderr = execute(command, env=self.env)
        if exit_code != 0:
            raise PostgreSQLError(
                command=f"{command}",
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
            )

    def gzip(self, filename, action="gzip"):
        """Run gzip or gunzip."""
        if action == "gzip":
            self.run("gzip", filename)
        elif action == "gunzip":
            self.run("gunzip", filename)

    def pgdump(self, filename):
        """Run pgdump."""
        params = [*self.db_params, "-d", self.database, "-f", filename]
        self.run("pg_dump", params)

    def psql(self, command=None, filename=None, database="postgres"):
        """Run psql command."""
        if command is not None:
            self.run("psql", [*self.db_params, "-d", database, "-c", command])
        elif filename is not None:
            self.run("psql", [*self.db_params, "-d", database, "-f", filename])

    def delete_and_create(self):
        """Delete and create a fresh database."""
        for command in self.DB_DUMP_CREATE:
            self.psql(command.format(database=self.database, user=self.user))

    def dump(
        self,
        output_directory: Path,
        tag: Optional[str] = None,
        delete: bool = False,
    ):
        """Dump database."""
        now = datetime.now()
        hostname = socket.gethostname()
        tag = f"-{tag}" if tag else ""

        filename = (
            output_directory
            / f"{self.database}-{hostname}-{now:%Y%m%d%H%M%S}{tag}.backup"
        )

        # Create output directory if it doesn't exist.
        os.makedirs(output_directory, exist_ok=True)

        # Delete backup file if exists
        if delete and os.path.isfile(filename):
            os.remove(filename)
        if delete and os.path.isfile(f"{filename}.gz"):
            os.remove(f"{filename}.gz")

        self.pgdump(filename)
        self.gzip(filename, action="gzip")
        return f"{filename}.gz"

    def load(self, filename):
        """Load database."""
        filename_without_ext, ext = os.path.splitext(filename)
        if ext == ".gz":
            self.gzip(filename, action="gunzip")
            filename = filename_without_ext

        self.delete_and_create()
        self.psql(filename=filename, database=self.database)
