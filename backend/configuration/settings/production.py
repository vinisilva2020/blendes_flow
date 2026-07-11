"""Strict settings for production deployments."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False
DATABASES = {"default": postgres_database()}  # noqa: F405


def require(condition, message):
    if not condition:
        raise ImproperlyConfigured(message)


require(ALLOWED_HOSTS, "DJANGO_ALLOWED_HOSTS must contain at least one host.")  # noqa: F405
require("*" not in ALLOWED_HOSTS, "Production does not allow wildcard hosts.")  # noqa: F405
require(
    all(origin.startswith("https://") for origin in CSRF_TRUSTED_ORIGINS),  # noqa: F405
    "Production CSRF trusted origins must use HTTPS.",
)
require(
    all(origin.startswith("https://") for origin in CORS_ALLOWED_ORIGINS),  # noqa: F405
    "Production CORS allowed origins must use HTTPS.",
)
require(
    DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql",  # noqa: F405
    "Production requires PostgreSQL.",
)
database_password = DATABASES["default"].get("PASSWORD", "")  # noqa: F405
require(
    len(database_password) >= 16 and "change-me" not in database_password,
    "Production requires a strong database password.",
)
require(
    len(SECRET_KEY) >= 50  # noqa: F405
    and "change-me" not in SECRET_KEY  # noqa: F405
    and SECRET_KEY != "unsafe-development-only-django-secret-key",  # noqa: F405
    "Production requires a strong DJANGO_SECRET_KEY.",
)
require(
    len(JWT_SIGNING_KEY.encode("utf-8")) >= 32  # noqa: F405
    and "change-me" not in JWT_SIGNING_KEY  # noqa: F405
    and JWT_SIGNING_KEY != "unsafe-development-only-jwt-signing-key",  # noqa: F405
    "Production requires a strong JWT_SIGNING_KEY.",
)
require(SECRET_KEY != JWT_SIGNING_KEY, "Django and JWT keys must be different.")  # noqa: F405

STATIC_ROOT = env("DJANGO_STATIC_ROOT", default="/var/www/static")  # noqa: F405
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", default="/var/www/media")  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int(  # noqa: F405
    "DJANGO_SECURE_HSTS_SECONDS",
    default=31536000,
)
require(SECURE_HSTS_SECONDS > 0, "Production requires HSTS.")
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
