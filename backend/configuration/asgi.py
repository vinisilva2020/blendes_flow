import os

from django.core.asgi import get_asgi_application

from configuration.environment import load_environment

load_environment()
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configuration.settings.base",
)

application = get_asgi_application()
