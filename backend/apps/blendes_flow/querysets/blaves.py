from apps.blendes_flow.models import Blave


def user_owned_blave_in_organization_queryset(organization):
    """Carrega uma blave dentro de uma organizacao ja autorizada."""
    return (
        Blave.objects.select_related("created_by_user")
        .prefetch_related("movement_statuses")
        .filter(organization_id=organization.id)
    )


def user_owned_blave_queryset(user):
    """Carrega uma blave acessivel pelo usuario com relacoes de uso frequente."""
    return (
        Blave.objects.select_related("organization", "created_by_user")
        .prefetch_related("movement_statuses")
        .filter(
            organization__created_by=user,
            created_by_user=user,
        )
    )


def organization_blaves_queryset(organization):
    """Lista blaves da organizacao evitando consultas extras de usuario e movimentos."""
    return (
        Blave.objects.filter(organization_id=organization.id)
        .select_related("created_by_user")
        .prefetch_related("movement_statuses")
        .order_by("-created_at")
    )
