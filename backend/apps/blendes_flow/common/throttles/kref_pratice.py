from rest_framework.throttling import UserRateThrottle


class KrefPraticeManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de praticas KREF."""

    scope = "kref_pratices_management"
