from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS must contain at least one host in production."
    )

STATIC_ROOT = env(  # noqa: F405
    "DJANGO_STATIC_ROOT",
    default="/var/www/static",
)
MEDIA_ROOT = env(  # noqa: F405
    "DJANGO_MEDIA_ROOT",
    default="/var/www/media",
)

# O Nginx é o único proxy confiável na rede Docker de borda.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Os padrões seguros pressupõem TLS. O exemplo atual, somente HTTP, desabilita
# essas opções explicitamente até o Nginx receber a configuração de TLS.
SECURE_SSL_REDIRECT = env.bool(  # noqa: F405
    "DJANGO_SECURE_SSL_REDIRECT",
    default=True,
)
SESSION_COOKIE_SECURE = env.bool(  # noqa: F405
    "DJANGO_SESSION_COOKIE_SECURE",
    default=True,
)
CSRF_COOKIE_SECURE = env.bool(  # noqa: F405
    "DJANGO_CSRF_COOKIE_SECURE",
    default=True,
)
SECURE_HSTS_SECONDS = env.int(  # noqa: F405
    "DJANGO_SECURE_HSTS_SECONDS",
    default=31536000,
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
