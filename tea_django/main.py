import os
import re
import sys
from pathlib import Path
from typing import Optional

from tea.utils import get_object


PYTHON_RE = re.compile(
    rf"""
^                        # Start
(.*?)                    # Any path.
{os.path.sep}            # Path separator.
python                   # Python executable.
(                        # Optional version.
    3 | 3\d+ | 3\.\d+
)?
(\.(exe|app))?           # Optional extension.
$                        # End
""",
    re.VERBOSE | re.IGNORECASE,
)


class Main:
    def __init__(
        self,
        app_name: str,
        app_path: Optional[str] = None,
        app_dir: Optional[Path] = None,
    ):
        """Create main entry function.

        Args:
            app_name: Name of the application. Used for the commandline name
                and path to the settings file.
            app_path: Dotted path to the Typer main app. If it's not provided
                `{app_name}.commands.app` will be used.
            app_dir: Optional path to the directory containing the application
                library. Used for adding that directory to PYTHONPATH if it's
                not already added.
        """

        self.app_name = app_name
        self.app_module = app_name.replace("-", "_")
        self.app_path = app_path or f"{self.app_module}.commands.app"
        self.app_dir = app_dir

    def __call__(self):
        if self.app_dir is not None:
            # Setup python path
            module_dir = str(self.app_dir.absolute())
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            python_path = os.environ.get("PYTHONPATH", "").strip()
            if python_path == "":
                os.environ.setdefault("PYTHONPATH", module_dir)
            else:
                if module_dir not in python_path.split(":"):
                    os.environ.setdefault(
                        "PYTHONPATH", f"{module_dir}:{python_path.lstrip(':')}"
                    )

        # Setup django setting module
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            f"{self.app_module}.settings",
        )

        # Setup django
        import django

        django.setup()

        args = sys.argv[:]
        # Purge the args from `python -m app` or `python ../app/__main__.py`.
        if PYTHON_RE.match(args[0]) is not None:
            args = args[1:]

        # Remove -m if it's called as `python -m`
        if args[0] == "-m":
            args = args[1:]

        # Rename the app from main file to app_name
        if args[0].endswith(f"{self.app_module}{os.path.sep}__main__.py"):
            args[0] = self.app_name

        # Check if it's a django manage command and run it
        if (
            len(args) >= 2
            and (
                args[0].endswith(self.app_name)
                or args[0].endswith(self.app_module)
            )
            and args[1] == "manage"
        ):
            from django.core.management import execute_from_command_line

            execute_from_command_line(args[:1] + args[2:])
        # If not run the application
        else:
            app = get_object(self.app_path)
            app()
