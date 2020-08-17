from typing import Optional, List

import typer
from django.core.management import execute_from_command_line

app = typer.Typer(name="db", help="Database commands.")


@app.command(
    help="Runs the command-line client for specified database, or the default "
    "database if none is provided."
)
def shell(
    parameters: Optional[List[str]] = typer.Argument(None),
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
    """Run database shell."""
    command = [
        "traktor",
        "dbshell",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if database is not None:
        command.extend(["--database", database])
    if parameters is not None and len(parameters) > 0:
        command.extend(parameters)
    execute_from_command_line(command)


@app.command()
def makemigrations(
    app_label: Optional[str] = typer.Argument(
        None, help="Specify the app label(s) to create migrations for."
    ),
    dry_run: bool = typer.Option(
        False,
        help="Just show what migrations would be made; don't actually write "
        "them.",
    ),
    merge: bool = typer.Option(
        False, help="Enable fixing of migration conflicts.",
    ),
    empty: bool = typer.Option(False, help="Create an empty migration."),
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    name: str = typer.Option(
        None,
        "-n",
        "--name",
        metavar="NAME",
        help="Use this name for migration file(s).",
    ),
    no_header: bool = typer.Option(
        False,
        "--no-header",
        help="Do not add header comments to new migration file(s).",
    ),
    check: bool = typer.Option(
        False,
        help="Exit with a non-zero status if model changes are missing "
        "migrations.",
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
    """Creates new migration(s) for apps."""
    command = [
        "traktor",
        "makemigrations",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if dry_run:
        command.append("--dry-run")
    if merge:
        command.append("--merge")
    if empty:
        command.append("--empty")
    if no_input:
        command.append("--no-input")
    if name is not None:
        command.extend(["--name", name])
    if no_header:
        command.append("--no-header")
    if check:
        command.append("--check")
    if app_label is not None:
        command.append(app_label)
    execute_from_command_line(command)


@app.command(
    help="Updates database schema. Manages both apps with migrations and those"
    " without."
)
def migrate(
    app_label: Optional[str] = typer.Argument(
        None, help="App label of an application to synchronize the state."
    ),
    migration_name: Optional[str] = typer.Argument(
        None,
        help="Database state will be brought to the state after that "
        "migration. Use the name 'zero' to un-apply all migrations.",
    ),
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    fake: bool = typer.Option(
        False, help="Mark migrations as run without actually running them.",
    ),
    fake_initial: bool = typer.Option(
        False,
        help="Detect if tables already exist and fake-apply initial "
        "migrations if so. Make sure that the current database schema matches "
        "your initial migration before using this flag. Django will only check"
        " for an existing table name.",
    ),
    plan: bool = typer.Option(
        False,
        help="Shows a list of the migration actions that will be performed.",
    ),
    run_syncdb: bool = typer.Option(
        False, help="Creates tables for apps without migrations."
    ),
    check: bool = typer.Option(
        False,
        help="Exits with a non-zero status if un-applied migrations exist.",
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
    """Run migrations."""
    command = [
        "traktor",
        "migrate",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if no_input:
        command.append("--no-input")
    if database is not None:
        command.extend(["--database", database])
    if fake:
        command.append("--fake")
    if fake_initial:
        command.append("--fake-initial")
    if plan:
        command.append("--plan")
    if run_syncdb:
        command.append("--run-syncdb")
    if check:
        command.append("--check")
    if app_label is not None:
        command.append(app_label)
    if migration_name is not None:
        command.append(migration_name)
    execute_from_command_line(command)


@app.command()
def showmigrations(
    app_label: Optional[List[str]] = typer.Argument(
        None, help="App labels of applications to limit the output to."
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    list_migrations: bool = typer.Option(
        False,
        "-l",
        "--list",
        help="Shows a list of all migrations and which are applied. With a "
        "verbosity level of 2 or above, the applied datetimes will be "
        "included.",
    ),
    plan: bool = typer.Option(
        False,
        "-p",
        "--plan",
        help="Shows all migrations in the order they will be applied. With a "
        "verbosity level of 2 or above all direct migration dependencies and "
        "reverse dependencies (run_before) will be included.",
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
    """Shows all available migrations for the current project."""
    command = [
        "traktor",
        "showmigrations",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if database:
        command.extend(["--database", database])
    if list_migrations:
        command.append("--list")
    if plan:
        command.append("--plan")
    if app_label is not None and len(app_label) > 0:
        command.extend(app_label)
    execute_from_command_line(command)


@app.command(
    help="Squashes an existing set of migrations (from first until specified) "
    "into a single new one."
)
def squashmigrations(
    app_label: str = typer.Argument(
        ..., help="App label of the application to squash migrations for."
    ),
    start_migration_name: str = typer.Argument(
        ...,
        help="Migrations will be squashed starting from and including this "
        "migration.",
    ),
    migration_name: str = typer.Argument(
        ...,
        help="Migrations will be squashed until and including this migration.",
    ),
    no_optimize: bool = typer.Option(
        False,
        "--no-optimize",
        help="Do not try to optimize the squashed operations.",
    ),
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    squashed_name: str = typer.Option(
        None,
        metavar="SQUASHED_NAME",
        help="Sets the name of the new squashed migration.",
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
    """Squash migrations."""
    command = [
        "traktor",
        "squashmigrations",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if no_optimize:
        command.append("--no-optimize")
    if no_input:
        command.append("--no-input")
    if squashed_name is not None:
        command.extend(["--squashed-name", squashed_name])
    command.extend([app_label, start_migration_name, migration_name])
    execute_from_command_line(command)


@app.command()
def createcachetable(
    table_name: Optional[str] = typer.Argument(
        None,
        help="Optional table names. Otherwise, settings.CACHES is used to "
        "find cache tables.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Does not create the table, just prints the SQL that would be "
        "run.",
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
    """Creates the tables needed to use the SQL cache backend."""
    command = [
        "traktor",
        "createcachetable",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if database is not None:
        command.extend(["--database", database])
    if dry_run:
        command.append("--dry-run")
    if table_name is not None:
        command.append(table_name)
    execute_from_command_line(command)


@app.command(
    help="Can be run as a cronjob or directly to clean out expired sessions "
    "(only with the database backend at the moment)."
)
def clearsessions(
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
    """Delete expired sessions."""
    execute_from_command_line(
        [
            "traktor",
            "clearsessions",
            "--force-color",
            "--verbosity",
            str(verbosity),
        ]
    )


@app.command(
    help="Output the contents of the database as a fixture of the given format"
    " (using each model's default manager unless --all is specified)."
)
def dumpdata(
    app_label: Optional[str] = typer.Argument(
        None,
        metavar="app_label[.ModelName]",
        help="Restricts dumped data to the specified app_label or app_"
        "label.ModelName.",
    ),
    fmt: str = typer.Option(
        None,
        "--format",
        metavar="FORMAT",
        help="Specifies the output serialization format for fixtures.",
    ),
    indent: int = typer.Option(
        4,
        metavar="INDENT",
        help="Specifies the indent level to use when pretty-printing output.",
    ),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "-e",
        "--exclude",
        metavar="EXCLUDE",
        help="An app_label or app_label.ModelName to exclude (use multiple "
        "--exclude to exclude multiple apps/models).",
    ),
    natural_foreign: bool = typer.Option(
        False,
        "--natural-foreign",
        help="Use natural foreign keys if they are available.",
    ),
    natural_primary: bool = typer.Option(
        True,
        "--natural-primary",
        help="Use natural primary keys if they are available.",
    ),
    all: bool = typer.Option(
        False,
        "-a",
        "--all",
        help="Use Django's base manager to dump all models stored in the "
        "database, including those that would otherwise be filtered or "
        "modified by a custom manager.",
    ),
    pks: str = typer.Option(
        None,
        metavar="PRIMARY_KEYS",
        help="Only dump objects with given primary keys. Accepts a "
        "comma-separated list of keys. This option only works when you "
        "specify one model.",
    ),
    output: str = typer.Option(
        None,
        metavar="OUTPUT",
        help="Specifies file to which the output is written.",
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
        "dumpdata",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if fmt is not None:
        command.extend(["--format", fmt])
    if indent is not None:
        command.extend(["--indent", str(indent)])
    if database is not None:
        command.extend(["--database", database])
    if exclude is not None and len(exclude) > 0:
        for excl in exclude:
            command.extend(["--exclude", excl])
    if natural_foreign:
        command.append("--natural-foreign")
    if natural_primary:
        command.append("--natural-primary")
    if all:
        command.append("--all")
    if pks is not None:
        command.extend(["--pks", pks])
    if output is not None:
        command.extend(["--output", output])
    if app_label is not None:
        command.append(app_label)
    execute_from_command_line(command)


@app.command()
def loaddata(
    fixture: str = typer.Argument(..., help="Fixture labels."),
    database: str = typer.Option(
        None,
        metavar="DATABASE",
        help="Nominates a database onto which to open a shell. Defaults to "
        "the 'default' database.",
    ),
    app: str = typer.Option(
        None,
        metavar="APP_LABEL",
        help="Only look for fixtures in the specified app.",
    ),
    ignore_non_existent: bool = typer.Option(
        False,
        "-i",
        "--ignorenonexistent",
        help="Ignores entries in the serialized data for fields that do not "
        "currently exist on the model.",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "-e",
        "--exclude",
        metavar="EXCLUDE",
        help="An app_label or app_label.ModelName to exclude (use multiple "
        "--exclude to exclude multiple apps/models).",
    ),
    fmt: str = typer.Option(
        None,
        "--format",
        metavar="FORMAT",
        help="Format of serialized data when reading from stdin.",
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
    """Installs the named fixture(s) in the database."""
    command = [
        "traktor",
        "loaddata",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if database is not None:
        command.extend(["--database", database])
    if app is not None:
        command.extend(["--app", app])
    if ignore_non_existent:
        command.append("--ignorenonexistent")
    if exclude is not None and len(exclude) > 0:
        for excl in exclude:
            command.extend(["--exclude", excl])
    if fmt is not None:
        command.extend(["--format", fmt])
    command.append(fixture)
    execute_from_command_line(command)
