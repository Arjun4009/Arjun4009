from __future__ import annotations

import importlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if python-dotenv is available. The project still runs without it.
if importlib.util.find_spec("dotenv"):
    from dotenv import load_dotenv  # type: ignore

    load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-ops-suite-key")
DEBUG = os.environ.get("DEBUG", "True").lower() in {"1", "true", "yes", "on"}
ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,0.0.0.0,*").split(",") if host.strip()]

VERSION = os.environ.get("OPS_SUITE_VERSION", "1.0.0")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ops_suite.activitylog",
    "ops_suite.transitions",
    "ops_suite.offboarding",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "ops_suite.activitylog.middleware.ActivityLogMiddleware",
]

ROOT_URLCONF = "ops_suite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ops_suite.wsgi.application"
ASGI_APPLICATION = "ops_suite.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS: list[Path] = []
static_dir = BASE_DIR / "static"
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
    },
}
