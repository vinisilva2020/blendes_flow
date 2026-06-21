from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = env.list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "[::1]"],
)
CORS_ALLOWED_ORIGINS = env.list(  # noqa: F405
    "DJANGO_CORS_ALLOWED_ORIGINS",
    default=["http://localhost:5173", "http://127.0.0.1:5173"],
)
CORS_ALLOW_CREDENTIALS = env.bool(  # noqa: F405
    "DJANGO_CORS_ALLOW_CREDENTIALS",
    default=True,
)

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
