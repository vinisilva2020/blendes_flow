"""Settings used by the automated test suite.

This module deliberately uses an in-memory SQLite database so tests never
connect to, write to, or migrate the real development/production database.
"""

import os

os.environ["DJANGO_SECRET_KEY"] = "test-secret-key"
os.environ["JWT_SIGNING_KEY"] = "test-jwt-signing-key-with-at-least-32-bytes"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from .base import *  # noqa: F403

DEBUG = False
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "NAME": ":memory:",
        },
    },
}

MIGRATION_MODULES = {
    "blendes": None,
    "organizations": None,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "blendes-flow-tests",
    },
}

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_THROTTLE_RATES": {
        **REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"],  # noqa: F405
        "auth_login": "1000/minute",
        "auth_refresh": "1000/minute",
        "blaves_management": "1000/minute",
        "boundaries_management": "1000/minute",
        "boundaries_global_list": "1000/minute",
        "schapters_management": "1000/minute",
        "schapters_global_list": "1000/minute",
        "facet_descriptions_management": "1000/minute",
    },
}
