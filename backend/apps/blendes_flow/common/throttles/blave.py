from rest_framework.throttling import UserRateThrottle


class BlaveManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de blaves."""

    scope = "blaves_management"
