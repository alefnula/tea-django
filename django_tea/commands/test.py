from typing import List, Optional

import typer
from django.core.management import execute_from_command_line

app = typer.Typer(name="test", help="Testing helper commands.")


@app.command(
    help="Discover and run tests in the specified modules or the current "
    "directory."
)
def run(
    test_label: Optional[str] = typer.Argument(
        None,
        help="Module paths to test; can be modulename, modulename.TestCase or "
        "modulename.TestCase.test_method",
    ),
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    fail_fast: bool = typer.Option(
        False, help="Stop running the test suite after first failed test.",
    ),
    test_runner: str = typer.Option(
        None,
        metavar="TESTRUNNER",
        help="Use specified test runner class instead of the one specified by "
        "the TEST_RUNNER setting.",
    ),
    top_level_directory: str = typer.Option(
        None,
        "-t",
        "--top-level-directory",
        metavar="TOP_LEVEL",
        help="Top level of project for unittest discovery.",
    ),
    pattern: str = typer.Option(
        None,
        "-p",
        "--pattern",
        metavar="PATTERN",
        help="The test matching pattern. Defaults to test*.py.",
    ),
    keep_db: bool = typer.Option(
        False, help="Preserves the test DB between runs.",
    ),
    reverse: bool = typer.Option(
        False, "-r", "--reverse", help="Reverses test cases order."
    ),
    debug_mode: bool = typer.Option(
        False, help="Sets settings.DEBUG to True."
    ),
    debug_sql: bool = typer.Option(
        False,
        "-d",
        "--debug-sql",
        help="Prints logged SQL queries on failure.",
    ),
    parallel: int = typer.Option(
        0, metavar="[N]", help="Run tests using up to N parallel processes."
    ),
    tag: str = typer.Option(
        None,
        metavar="TAG",
        help="Run only tests with the specified tag. Can be used multiple "
        "times.",
    ),
    exclude_tag: List[str] = typer.Option(
        None,
        metavar="EXCLUDE_TAGS",
        help="Do not run tests with the specified tag. Can be used multiple "
        "times.",
    ),
    pdb: bool = typer.Option(
        False,
        help="Runs a debugger (pdb, or ipdb if installed) on error or "
        "failure.",
    ),
    buffer: bool = typer.Option(
        False, "-b", "--buffer", help="Discard output from passing tests."
    ),
    k: List[str] = typer.Option(
        None,
        "-k",
        metavar="TEST_NAME_PATTERNS",
        help="Only run test methods and classes that match the pattern or "
        "substring. Can be used multiple times. Same as unittest -k option.",
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
    """Run tests."""
    command = [
        "traktor",
        "test",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if no_input:
        command.append("--no-input")
    if fail_fast:
        command.append("--failfast")
    if test_runner is not None:
        command.extend(["--testrunner", test_runner])
    if top_level_directory is not None:
        command.extend(["--top-level-directory", top_level_directory])
    if pattern is not None:
        command.extend(["--pattern", pattern])
    if keep_db:
        command.append("--keepdb")
    if reverse:
        command.append("--reverse")
    if debug_mode:
        command.append("--debug-mode")
    if debug_sql:
        command.append("--debug-sql")
    if parallel > 0:
        command.extend(["--parallel", str(parallel)])
    if tag is not None:
        command.extend(["--tag", tag])
    if exclude_tag is not None and len(exclude_tag) > 0:
        for tag in exclude_tag:
            command.extend(["--exclude-tag", tag])
    if pdb:
        command.append("--pdb")
    if buffer:
        command.append("--buffer")
    if k is not None and len(k) > 0:
        for name in k:
            command.extend(["-k", name])
    if test_label is not None:
        command.append(test_label)
    execute_from_command_line(command)


@app.command()
def server(
    fixture: str,
    no_input: bool = typer.Option(
        False,
        "--noinput",
        "--no-input",
        help="Do NOT prompt the user for input of any kind.",
    ),
    port: str = typer.Option(
        None,
        metavar="ADDRPORT",
        help="Port number or ip_address:port to run the server on.",
    ),
    ipv6: bool = typer.Option(False, help="Use an IPv6 address.",),
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
    """Runs a development server with data from the given fixture(s)."""
    command = [
        "traktor",
        "testserver",
        "--force-color",
        "--verbosity",
        str(verbosity),
    ]
    if no_input:
        command.append("--no-input")
    if port:
        command.extend(["--addrport", port])
    if ipv6:
        command.append("--ipv6")
    command.append(fixture)
    execute_from_command_line(command)
