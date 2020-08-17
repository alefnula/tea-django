__all__ = ["auth_app", "db_app", "django_app", "server_app", "test_app"]

from django_tea.commands.auth import app as auth_app
from django_tea.commands.db import app as db_app
from django_tea.commands.django_app import app as django_app
from django_tea.commands.server import app as server_app
from django_tea.commands.test import app as test_app
