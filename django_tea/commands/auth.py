from typing import Optional

import typer
from django.core.management import execute_from_command_line

app = typer.Typer(name="auth", help="Auth commands.")


@app.command()
def changepassword(
    username: Optional[str] = typer.Argument(
        None,
        help=" Username to change password for; by default, it's the current "
        "username.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    verbosity: int = typer.Option(
        1,
        "-v",
        "--verbosity",
        metavar="{0, 1, 2, 3}",
        min=0,
        max=3,
        help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose "
        "output, 3=very verbose output)",
    ),
):
    """Change a user's password for django.contrib.auth."""
    command = [
        "traktor",
        "changepassword",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if database is not None:
        command.extend(["--database", database])
    if username is not None:
        command.append(username)
    execute_from_command_line(command)


@app.command()
def createsuperuser(
    username: str = typer.Option(
        None, metavar="USERNAME", help="Specifies the login for the superuser."
    ),
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind. You must use "
        "--username with --noinput, along with an option for any other "
        "required field. Superusers created with --noinput will not be able "
        "to log in until they're given a valid password.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Specifies the database to use. Default is 'default'.",
    ),
    email: str = typer.Option(
        None, metavar="EMAIL", help="Specifies the email for the superuser."
    ),
    verbosity: int = typer.Option(
        1,
        "-v",
        "--verbosity",
        metavar="{0, 1, 2, 3}",
        min=0,
        max=3,
        help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose "
        "output, 3=very verbose output)",
    ),
):
    """Used to create a superuser."""
    command = [
        "traktor",
        "createsuperuser",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if username is not None:
        command.extend(["--username", username])
    if no_input:
        command.append("--no-input")
    if database is not None:
        command.extend(["--database", database])
    if email is not None:
        command.extend(["--email", email])
    execute_from_command_line(command)
