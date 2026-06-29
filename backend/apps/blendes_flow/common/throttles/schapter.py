from rest_framework.throttling import UserRateThrottle


class SchapterManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de schapters."""

    scope = "schapters_management"


class SchapterGlobalListRateThrottle(UserRateThrottle):
    """Limita consultas globais de nomes de schapters."""

    scope = "schapters_global_list"
