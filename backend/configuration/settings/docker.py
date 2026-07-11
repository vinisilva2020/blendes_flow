"""Settings for the reproducible local Docker environment."""

from .base import *  # noqa: F403

DEBUG = False

DATABASES = {"default": postgres_database()}  # noqa: F405

ALLOWED_HOSTS = env.list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "nginx"],
)
CSRF_TRUSTED_ORIGINS = env.list(  # noqa: F405
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=["http://localhost", "http://127.0.0.1"],
)

STATIC_ROOT = env("DJANGO_STATIC_ROOT", default="/var/www/static")  # noqa: F405
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", default="/var/www/media")  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
