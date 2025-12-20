"""Settings package.

Importing ``portfolio_project.settings`` will load development settings by
default. For production deployments set the environment variable
``DJANGO_SETTINGS_MODULE`` to ``portfolio_project.settings.prod``.
"""
from .dev import *  # noqa: F401,F403
