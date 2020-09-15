import os
from pathlib import Path
from typing import Optional

import typer
from tea_django.database.postgresql import PostgreSQL


def dump(
    tag: Optional[str] = typer.Option(
        None,
        "-t",
        "--tag",
        help="Tag that will be added to the end of the filename.",
    ),
    output_directory: Path = typer.Option(
        os.getcwd(),
        "-o",
        "--output-directory",
        help="File output directory. Default: Current working directory.",
        dir_okay=True,
        file_okay=False,
    ),
    delete: bool = typer.Option(
        False, "-d", "--delete", help="Delete backup file if exists."
    ),
):
    """Dump PostgreSQL database."""
    postgres = PostgreSQL()
    postgres.dump(output_directory=output_directory, tag=tag, delete=delete)


def load(filename: str = typer.Argument(..., help="Dump file to load")):
    """Load PostgreSQL database dump."""
    postgres = PostgreSQL()
    postgres.load(filename=filename)
