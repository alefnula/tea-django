import typer
from django.core.management import execute_from_command_line

app = typer.Typer(name="server", help="Web server commands.")


@app.command(
    help="Starts a lightweight Web server for development and also serves "
    "static files."
)
def run(
    port: str = typer.Argument(
        "127.0.0.1:8000", help="Optional port number or ip_address:port"
    ),
    ipv6: bool = typer.Option(False, help="Tell traktor to use IPv6 address."),
    threading: bool = typer.Option(
        True, help="Tells traktor to use threading."
    ),
    reload: bool = typer.Option(
        True, help="Tells traktor to use the auto-reloader."
    ),
    static: bool = typer.Option(
        True, help="Tells app to automatically serve static files."
    ),
    insecure: bool = typer.Option(
        False, help="Allows serving static files even if DEBUG is False."
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
    """Start development server."""
    command = [
        "traktor",
        "runserver",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if ipv6:
        command.append("--ipv6")
    if not threading:
        command.append("--nothreading")
    if not reload:
        command.append("--noreload")
    if not static:
        command.append("--nostatic")
    if insecure:
        command.append("--insecure")
    command.append(port)
    execute_from_command_line(command)
