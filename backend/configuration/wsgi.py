import os

from django.core.wsgi import get_wsgi_application

from configuration.environment import load_environment

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configuration.settings.local",
)
load_environment()

application = get_wsgi_application()
