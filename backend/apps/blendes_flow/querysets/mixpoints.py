from apps.blendes_flow.models import ConcreteAction, Mixpoint


def user_concrete_action_queryset(user):
    """Busca acoes concretas acessiveis pelo usuario com a cadeia KREF carregada."""
    return ConcreteAction.objects.select_related(
        "kref_pratice",
        "kref_pratice__risk",
        "kref_pratice__risk__facet_description",
        "kref_pratice__risk__facet_description__schapter",
        "kref_pratice__risk__facet_description__schapter__boundary",
        "kref_pratice__risk__facet_description__schapter__boundary__blave",
        (
            "kref_pratice__risk__facet_description__schapter__boundary"
            "__blave__organization"
        ),
    ).filter(
        kref_pratice__risk__facet_description__schapter__boundary__blave__organization__created_by=user,
        kref_pratice__risk__facet_description__schapter__boundary__blave__created_by_user=user,
    )


def user_mixpoint_queryset(user):
    """Busca mixpoints acessiveis pelo usuario com a cadeia da acao carregada."""
    return Mixpoint.objects.select_related(
        "concrete_action",
        "concrete_action__kref_pratice",
        "concrete_action__kref_pratice__risk",
        "concrete_action__kref_pratice__risk__facet_description",
        "concrete_action__kref_pratice__risk__facet_description__schapter",
        (
            "concrete_action__kref_pratice__risk__facet_description__schapter"
            "__boundary"
        ),
        (
            "concrete_action__kref_pratice__risk__facet_description__schapter"
            "__boundary__blave"
        ),
        (
            "concrete_action__kref_pratice__risk__facet_description__schapter"
            "__boundary__blave__organization"
        ),
    ).filter(
        concrete_action__kref_pratice__risk__facet_description__schapter__boundary__blave__organization__created_by=user,
        concrete_action__kref_pratice__risk__facet_description__schapter__boundary__blave__created_by_user=user,
    )


def concrete_action_mixpoints_queryset(concrete_action):
    """Lista mixpoints da acao concreta com dados suficientes para resposta."""
    return (
        Mixpoint.objects.filter(concrete_action=concrete_action)
        .select_related(
            "concrete_action",
            "concrete_action__kref_pratice",
            "concrete_action__kref_pratice__risk",
            "concrete_action__kref_pratice__risk__facet_description",
        )
        .order_by("created_at")
    )
