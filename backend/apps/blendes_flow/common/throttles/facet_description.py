from rest_framework.throttling import UserRateThrottle


class FacetDescriptionManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de facet descriptions."""

    scope = "facet_descriptions_management"
