from rest_framework.throttling import UserRateThrottle


class MixpointManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de mixpoints."""

    scope = "mixpoints_management"
