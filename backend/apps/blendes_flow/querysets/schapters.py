from apps.blendes_flow.models import Boundary, Schapter


def boundary_in_blave_queryset(blave):
    """Busca uma boundary dentro da blave informada."""
    return Boundary.objects.filter(blave=blave)


def user_boundary_queryset(user):
    """Busca boundaries acessiveis pelo usuario com blave e organizacao carregadas."""
    return Boundary.objects.select_related("blave", "blave__organization").filter(
        blave__organization__created_by=user,
        blave__created_by_user=user,
    )


def user_schapter_queryset(user):
    """Busca schapters acessiveis pelo usuario com roles pre-carregadas."""
    return (
        Schapter.objects.select_related(
            "boundary",
            "boundary__blave",
            "boundary__blave__organization",
        )
        .prefetch_related("roles")
        .filter(
            boundary__blave__organization__created_by=user,
            boundary__blave__created_by_user=user,
        )
    )


def schapter_in_boundary_queryset(boundary):
    """Busca schapters dentro da boundary com roles pre-carregadas."""
    return (
        Schapter.objects.select_related("boundary", "boundary__blave")
        .prefetch_related("roles")
        .filter(boundary=boundary)
    )


def boundary_schapters_queryset(boundary):
    """Lista schapters da boundary evitando N+1 em boundary/blave/roles."""
    return (
        Schapter.objects.filter(boundary=boundary)
        .select_related("boundary", "boundary__blave")
        .prefetch_related("roles")
    )


def global_schapter_names_queryset():
    """Lista nomes globais de schapters de forma distinta e ordenada."""
    return Schapter.objects.order_by("name").values("name").distinct()


def schapter_name_queryset(boundary, name):
    """Centraliza a busca por nome para validar duplicidade na boundary."""
    return Schapter.objects.filter(boundary=boundary, name=name)
