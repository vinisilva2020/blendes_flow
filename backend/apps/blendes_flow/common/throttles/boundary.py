from rest_framework.throttling import UserRateThrottle


class BoundaryManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de boundaries."""

    scope = "boundaries_management"


class BoundaryGlobalListRateThrottle(UserRateThrottle):
    """Limita consultas globais de nomes de boundaries."""

    scope = "boundaries_global_list"
