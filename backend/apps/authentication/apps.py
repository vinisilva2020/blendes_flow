from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "apps.authentication"

    def ready(self):
        import apps.authentication.schema  # noqa: F401
