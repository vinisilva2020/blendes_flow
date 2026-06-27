"""Shared settings for every BlendESFlow environment."""

from datetime import timedelta
from importlib.util import find_spec
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

from configuration.environment import load_environment

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Process variables take precedence; backend/.env is only a local convenience.
load_environment()

env = environ.Env()


def env_or_file(name):
    """Read a secret from NAME or from the path stored in NAME_FILE."""
    value = env(name, default=None)
    if value:
        return value

    secret_file = env(f"{name}_FILE", default=None)
    if secret_file:
        secret_path = Path(secret_file)
        if not secret_path.is_absolute():
            secret_path = BASE_DIR / secret_path
        try:
            return secret_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise ImproperlyConfigured(
                f"Unable to read {name}_FILE: {secret_path}"
            ) from exc

    raise ImproperlyConfigured(f"Set {name} or {name}_FILE.")


SECRET_KEY = env_or_file("DJANGO_SECRET_KEY")

JWT_SIGNING_KEY = env_or_file("JWT_SIGNING_KEY")
if len(JWT_SIGNING_KEY.encode("utf-8")) < 32:
    raise ImproperlyConfigured("JWT_SIGNING_KEY must contain at least 32 bytes.")
if JWT_SIGNING_KEY == SECRET_KEY:
    raise ImproperlyConfigured(
        "JWT_SIGNING_KEY must be different from DJANGO_SECRET_KEY."
    )

JWT_ACCESS_TOKEN_LIFETIME_SECONDS = env.int(
    "JWT_ACCESS_TOKEN_LIFETIME_SECONDS",
    default=300,
)
if not 1 <= JWT_ACCESS_TOKEN_LIFETIME_SECONDS <= 900:
    raise ImproperlyConfigured(
        "JWT_ACCESS_TOKEN_LIFETIME_SECONDS must be between 1 and 900."
    )

AUTH_SESSION_LIFETIME_SECONDS = env.int(
    "AUTH_SESSION_LIFETIME_SECONDS",
    default=60 * 60 * 24 * 30,
)
if not 60 <= AUTH_SESSION_LIFETIME_SECONDS <= 60 * 60 * 24 * 90:
    raise ImproperlyConfigured(
        "AUTH_SESSION_LIFETIME_SECONDS must be between 60 and 7776000."
    )

GOOGLE_OAUTH_CLIENT_ID = env("GOOGLE_OAUTH_CLIENT_ID", default="")
GOOGLE_ALLOWED_HOSTED_DOMAIN = env("GOOGLE_ALLOWED_HOSTED_DOMAIN", default="")

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = env.bool("DJANGO_CORS_ALLOW_CREDENTIALS", default=False)
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
    "x-requested-with",
]
CORS_MAX_AGE = env.int("DJANGO_CORS_MAX_AGE", default=86400)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "apps.accounts.apps.AccountsConfig",
    "apps.authentication.apps.AuthenticationConfig",
    "apps.organizations.apps.OrganizationsConfig",
    "apps.blendes.apps.BlendesConfig",
    "drf_spectacular",
]

SILENCED_SYSTEM_CHECKS = []
if find_spec("psycopg") or find_spec("psycopg2"):
    INSTALLED_APPS.append("django.contrib.postgres")
else:
    SILENCED_SYSTEM_CHECKS.append("postgres.E005")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "configuration.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configuration.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "configuration.wsgi.application"
ASGI_APPLICATION = "configuration.asgi.application"

database_url = env("DATABASE_URL", default=None)
if database_url:
    DATABASES = {
        "default": environ.Env.db_url_config(database_url),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env_or_file("DB_PASSWORD"),
            "HOST": env("DB_HOST", default="database"),
            "PORT": env.int("DB_PORT", default=5432),
        },
    }

DATABASES["default"]["CONN_MAX_AGE"] = env.int(
    "DATABASE_CONN_MAX_AGE",
    default=0,
)
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT", default=str(BASE_DIR / "staticfiles"))

MEDIA_URL = "/media/"
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", default=str(BASE_DIR / "media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.authentication.models.SessionJWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": env(
            "API_ANON_THROTTLE_RATE",
            default="100/day",
        ),
        "user": env(
            "API_USER_THROTTLE_RATE",
            default="1000/day",
        ),
        "auth_login": env(
            "AUTH_LOGIN_THROTTLE_RATE",
            default="5/minute",
        ),
        "auth_refresh": env(
            "AUTH_REFRESH_THROTTLE_RATE",
            default="30/minute",
        ),
        "users_registration": env(
            "USERS_REGISTRATION_THROTTLE_RATE",
            default="5/hour",
        ),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Blendes Flow API",
    "DESCRIPTION": "API do Blendes Flow",
    "VERSION": "1.0.0",
}

# Simple JWT is limited to short-lived access tokens. Refresh tokens are opaque
# credentials managed by the application session model.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=JWT_ACCESS_TOKEN_LIFETIME_SECONDS,
    ),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": env("JWT_AUDIENCE", default="blendesflow-api"),
    "ISSUER": env("JWT_ISSUER", default="blendesflow-api"),
    "LEEWAY": env.int("JWT_LEEWAY_SECONDS", default=0),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "UPDATE_LAST_LOGIN": False,
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "CHECK_USER_IS_ACTIVE": True,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "{asctime} {levelname} {name} "
                "process={process:d} thread={thread:d} {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
