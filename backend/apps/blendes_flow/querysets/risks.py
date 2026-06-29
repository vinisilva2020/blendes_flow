from apps.blendes_flow.models import Boundary, FacetDescription, Risk, Schapter


def boundary_in_blave_queryset(blave):
    """Busca uma boundary dentro da blave informada."""
    return Boundary.objects.filter(blave=blave)


def schapter_in_boundary_queryset(boundary):
    """Busca uma schapter dentro da boundary informada."""
    return Schapter.objects.select_related("boundary", "boundary__blave").filter(
        boundary=boundary,
    )


def facet_description_in_schapter_queryset(schapter):
    """Busca facet descriptions dentro da schapter com contexto carregado."""
    return FacetDescription.objects.select_related(
        "schapter",
        "schapter__boundary",
        "schapter__boundary__blave",
    ).filter(schapter=schapter)


def risk_in_facet_description_queryset(facet_description):
    """Busca riscos dentro da facet description com contexto carregado."""
    return Risk.objects.select_related(
        "facet_description",
        "facet_description__schapter",
        "facet_description__schapter__boundary",
        "facet_description__schapter__boundary__blave",
    ).filter(facet_description=facet_description)


def user_facet_description_queryset(user):
    """Busca facet descriptions acessiveis pelo usuario."""
    return FacetDescription.objects.select_related(
        "schapter",
        "schapter__boundary",
        "schapter__boundary__blave",
        "schapter__boundary__blave__organization",
    ).filter(
        schapter__boundary__blave__organization__created_by=user,
        schapter__boundary__blave__created_by_user=user,
    )


def user_risk_queryset(user):
    """Busca riscos acessiveis pelo usuario com toda a cadeia carregada."""
    return Risk.objects.select_related(
        "facet_description",
        "facet_description__schapter",
        "facet_description__schapter__boundary",
        "facet_description__schapter__boundary__blave",
        "facet_description__schapter__boundary__blave__organization",
    ).filter(
        facet_description__schapter__boundary__blave__organization__created_by=user,
        facet_description__schapter__boundary__blave__created_by_user=user,
    )


def facet_description_risks_queryset(facet_description):
    """Lista riscos da facet description com ordenacao funcional do dominio."""
    return (
        Risk.objects.filter(facet_description=facet_description)
        .select_related(
            "facet_description",
            "facet_description__schapter",
            "facet_description__schapter__boundary",
            "facet_description__schapter__boundary__blave",
        )
        .order_by("created_at", "priority_position")
    )
