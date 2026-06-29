from rest_framework.throttling import UserRateThrottle


class RiskManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de riscos."""

    scope = "risks_management"
