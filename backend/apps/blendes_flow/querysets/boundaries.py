from apps.blendes_flow.models import Blave, Boundary


def user_owned_blave_for_boundaries_queryset(user):
    """Busca blaves autorizadas para operacoes de boundary."""
    return Blave.objects.select_related("organization", "created_by_user").filter(
        organization__created_by=user,
        created_by_user=user,
    )


def boundary_in_blave_queryset(blave):
    """Busca boundaries dentro da blave com dados do pai carregados."""
    return Boundary.objects.select_related("blave", "outer_boundary").filter(
        blave=blave,
    )


def user_boundary_queryset(user):
    """Busca boundaries acessiveis pelo usuario derivando a blave pelo relacionamento."""
    return Boundary.objects.select_related(
        "blave",
        "blave__organization",
        "outer_boundary",
    ).filter(
        blave__organization__created_by=user,
        blave__created_by_user=user,
    )


def blave_boundaries_queryset(blave):
    """Lista boundaries de uma blave sem causar N+1 no pai contextual."""
    return Boundary.objects.filter(blave=blave).select_related(
        "blave",
        "outer_boundary",
    )


def global_boundary_names_queryset():
    """Lista nomes globais de boundaries de forma distinta e ordenada."""
    return Boundary.objects.order_by("name").values("name").distinct()


def boundary_name_queryset(blave, name):
    """Centraliza a busca por nome para validar duplicidade na blave."""
    return Boundary.objects.filter(blave=blave, name=name)
