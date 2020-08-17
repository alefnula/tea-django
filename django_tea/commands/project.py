import enum
from typing import List, Optional

import typer
from django.core.management import execute_from_command_line

app = typer.Typer(name="project", help="Project level helper commands.")


@app.command()
def collectstatic(
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    no_post_process: bool = typer.Option(
        False, help="Do NOT post process collected files."
    ),
    ignore: List[str] = typer.Option(
        None,
        "-i",
        "--ignore",
        metavar="PATTERN",
        help="Ignore files or directories matching this glob-style pattern. "
        "Use multiple times to ignore more.",
    ),
    dry_run: bool = typer.Option(
        False,
        "-n",
        "--dry-run",
        help="Do everything except modify the filesystem.",
    ),
    clear: bool = typer.Option(
        False,
        "-c",
        "--clear",
        help="Clear the existing files using the storage before trying to copy"
        " or link the original file.",
    ),
    link: bool = typer.Option(
        False,
        "-l",
        "--link",
        help="Create a symbolic link to each file instead of copying.",
    ),
    no_default_ignore: bool = typer.Option(
        False,
        help="Don't ignore the common private glob-style patterns (defaults to"
        " 'CVS', '.*' and '*~').",
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
    """Collect static files in a single location."""
    command = [
        "traktor",
        "collectstatic",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if no_input:
        command.append("--no-input")
    if no_post_process:
        command.append("--no-post-process")
    if ignore is not None and len(ignore) > 0:
        for pattern in ignore:
            command.extend(["--ignore", pattern])
    if dry_run:
        command.append("--dry-run")
    if clear:
        command.append("--clear")
    if link:
        command.append("--link")
    if no_default_ignore:
        command.append("--no-default-ignore")

    execute_from_command_line(command)


class FailLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


@app.command()
def check(
    app_label: Optional[str] = typer.Argument(None),
    tag: str = typer.Option(
        None,
        "-t",
        "--tag",
        metavar="TAGS",
        help="Run only checks labeled with given tag.",
    ),
    list_tags: bool = typer.Option(False, help="List available tags."),
    deploy: bool = typer.Option(False, help="Check deployment settings.",),
    fail_level: FailLevel = typer.Option(
        FailLevel.ERROR,
        help="Message level that will cause the command to exit with a "
        "non-zero status.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASES" "--clear",
        help="Run database related checks against these aliases.",
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
    """Checks the entire Django project for potential problems."""
    command = [
        "traktor",
        "check",
        "--force-color",
        "--fail-level",
        fail_level.value,
        "--verbosity",
        str(verbosity),
    ]
    if tag is not None:
        command.extend(["--tag", tag])
    if list_tags:
        command.append("--list-tags")
    if deploy:
        command.append("--deploy")
    if database is not None:
        command.extend(["--database", database])
    if app_label is not None:
        command.append(app_label)
    execute_from_command_line(command)


@app.command(
    help="Creates a Django app directory structure for the given app name in "
    "the current directory or optionally in the given directory."
)
def start_app(
    name: str,
    directory: Optional[str] = typer.Argument(
        None, help="Optional destination directory"
    ),
    template: str = typer.Option(
        None,
        metavar="TEMPLATE",
        help="The path or URL to load the template from.",
    ),
    extension: List[str] = typer.Option(
        None,
        "-e",
        "--extension",
        metavar="EXTENSIONS",
        help="The file extension(s) to render (default: 'py'). Separate "
        "multiple extensions with commas, or use -e multiple times.",
    ),
    files: List[str] = typer.Option(
        False,
        "-n",
        "--name",
        metavar="FILES",
        help="The file name(s) to render. Separate multiple file names with "
        "commas, or use -n multiple times.",
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
    """Start a new django app."""
    command = [
        "traktor",
        "startapp",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if template is not None:
        command.extend(["--template", template])
    if extension is not None and len(extension) > 0:
        for ext in extension:
            command.extend(["--extension", ext])
    if files is not None and len(files) > 0:
        for file in files:
            command.extend(["--name", file])
    command.append(name)
    if directory is not None:
        command.append(directory)
    execute_from_command_line(command)


class DiffOutput(str, enum.Enum):
    hash = "hash"
    unified = "unified"


@app.command(
    help="Displays differences between the current settings.py and project's "
    "default settings."
)
def diff_settings(
    all: bool = typer.Option(
        False,
        help="Display all settings, regardless of their value. In 'hash' "
        "mode, default values are prefixed by ',  ###'.",
    ),
    default: str = typer.Option(
        None,
        metavar="MODULE",
        help="The settings module to compare the current settings against. "
        "Leave empty to compare against Django's default settings.",
    ),
    output: DiffOutput = typer.Option(
        DiffOutput.unified,
        help="Selects the output format. 'hash' mode displays each changed "
        "setting, with the settings that don't appear in the defaults "
        "followed by ###. 'unified' mode prefixes the default setting with a "
        "minus sign, followed by the changed setting prefixed with a plus "
        "sign.",
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
    """Create a settings diff.."""
    command = [
        "traktor",
        "diffsettings",
        "--force-color",
        "--verbosity",
        str(verbosity),
        "--output",
        output.value,
    ]
    if all:
        command.append("--all")
    if default is not None:
        command.extend(["--default", default])
    execute_from_command_line(command)


class ShellInterface(str, enum.Enum):
    ipython = "ipython"
    bpython = "bpython"
    python = "python"


@app.command(
    help="Runs a Python interactive interpreter. Tries to use IPython or "
    "bpython, if one of them is available. Any standard input is executed as "
    "code."
)
def shell(
    no_startup: bool = typer.Option(
        False,
        help="When using plain Python, ignore the PYTHONSTARTUP environment "
        "variable and ~/.pythonrc.py script.",
    ),
    interface: ShellInterface = typer.Option(
        ShellInterface.ipython,
        "-i",
        "--interface",
        help="Specify an interactive interpreter interface. Available options:"
        " 'ipython', 'bpython', and 'python'.",
    ),
    cmd: str = typer.Option(
        None,
        "-c",
        "--command",
        metavar="COMMAND",
        help="Instead of opening an interactive shell, run a command as "
        "Django and exit.",
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
    """Run ipython shell."""
    command = [
        "traktor",
        "shell",
        "--force-color",
        "--verbosity",
        str(verbosity),
        "--interface",
        interface.value,
    ]
    if no_startup:
        command.append("--no-startup")
    if cmd is not None:
        command.extend(["--command", cmd])
    execute_from_command_line(command)
