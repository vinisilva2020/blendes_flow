from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """Limita tentativas anônimas de autenticação por origem."""

    scope = "auth_login"


class RefreshRateThrottle(AnonRateThrottle):
    """Limita tentativas anônimas de renovação de credenciais por origem."""

    scope = "auth_refresh"
