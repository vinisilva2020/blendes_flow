from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS must contain at least one host in beta."
    )

STATIC_ROOT = env(  # noqa: F405
    "DJANGO_STATIC_ROOT",
    default="/var/www/static",
)
MEDIA_ROOT = env(  # noqa: F405
    "DJANGO_MEDIA_ROOT",
    default="/var/www/media",
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

SECURE_SSL_REDIRECT = env.bool(  # noqa: F405
    "DJANGO_SECURE_SSL_REDIRECT",
    default=False,
)
SESSION_COOKIE_SECURE = env.bool(  # noqa: F405
    "DJANGO_SESSION_COOKIE_SECURE",
    default=False,
)
CSRF_COOKIE_SECURE = env.bool(  # noqa: F405
    "DJANGO_CSRF_COOKIE_SECURE",
    default=False,
)
SECURE_HSTS_SECONDS = env.int(  # noqa: F405
    "DJANGO_SECURE_HSTS_SECONDS",
    default=0,
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
