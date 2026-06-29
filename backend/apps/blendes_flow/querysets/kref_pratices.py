from apps.blendes_flow.models import KrefPratice, Risk


def user_risk_queryset(user):
    """Busca riscos acessiveis pelo usuario para gerenciar praticas KREF."""
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


def user_kref_pratice_queryset(user):
    """Busca praticas KREF acessiveis com a cadeia de risco carregada."""
    return KrefPratice.objects.select_related(
        "risk",
        "risk__facet_description",
        "risk__facet_description__schapter",
        "risk__facet_description__schapter__boundary",
        "risk__facet_description__schapter__boundary__blave",
        "risk__facet_description__schapter__boundary__blave__organization",
    ).filter(
        risk__facet_description__schapter__boundary__blave__organization__created_by=user,
        risk__facet_description__schapter__boundary__blave__created_by_user=user,
    )


def risk_kref_pratices_queryset(risk):
    """Lista praticas KREF do risco com contexto suficiente para serializacao."""
    return (
        KrefPratice.objects.filter(risk=risk)
        .select_related(
            "risk",
            "risk__facet_description",
            "risk__facet_description__schapter",
            "risk__facet_description__schapter__boundary",
            "risk__facet_description__schapter__boundary__blave",
        )
        .order_by("created_at", "pratice")
    )
