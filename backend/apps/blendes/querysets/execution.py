from apps.blendes.models.execution import Blave


def blave_api_queryset():
    """Retorna blaves com relacionamentos necessários para resposta da API."""
    return (
        Blave.objects.select_related("created_by_user")
        .prefetch_related("movement_statuses")
        .order_by("-created_at")
    )


def list_organization_blaves_queryset(organization):
    """Lista blaves pertencentes a uma organização já validada."""
    return blave_api_queryset().filter(organization=organization)


def find_organization_blave_queryset(organization, blave_id):
    """Busca uma blave pelo id dentro da organização selecionada."""
    return blave_api_queryset().filter(
        id=blave_id,
        organization=organization,
    )


def find_organization_blave_for_update_queryset(organization, blave_id):
    """Busca uma blave para escrita sem carregar relações desnecessárias."""
    return Blave.objects.filter(
        id=blave_id,
        organization=organization,
    )
