"""WSGI config for ops_suite project."""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ops_suite.settings")

application = get_wsgi_application()
