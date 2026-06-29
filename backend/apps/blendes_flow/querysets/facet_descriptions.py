from apps.blendes_flow.models import Boundary, FacetDescription, Schapter


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


def user_schapter_queryset(user):
    """Busca schapters acessiveis pelo usuario derivando blave e organizacao."""
    return Schapter.objects.select_related(
        "boundary",
        "boundary__blave",
        "boundary__blave__organization",
    ).filter(
        boundary__blave__organization__created_by=user,
        boundary__blave__created_by_user=user,
    )


def user_facet_description_queryset(user):
    """Busca facet descriptions acessiveis pelo usuario com toda a cadeia carregada."""
    return FacetDescription.objects.select_related(
        "schapter",
        "schapter__boundary",
        "schapter__boundary__blave",
        "schapter__boundary__blave__organization",
    ).filter(
        schapter__boundary__blave__organization__created_by=user,
        schapter__boundary__blave__created_by_user=user,
    )


def schapter_facet_descriptions_queryset(schapter):
    """Lista facet descriptions da schapter ordenadas pela faceta."""
    return (
        FacetDescription.objects.filter(schapter=schapter)
        .select_related("schapter", "schapter__boundary", "schapter__boundary__blave")
        .order_by("facet")
    )


def facet_descriptions_by_facets_queryset(schapter, facet_names):
    """Busca facetas existentes para impedir duplicidade em lote."""
    return FacetDescription.objects.filter(
        schapter=schapter,
        facet__in=facet_names,
    )
