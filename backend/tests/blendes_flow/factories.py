from itertools import count

from apps.blendes_flow.models import (
    ActorType,
    Blave,
    Boundary,
    ConcreteAction,
    FacetDescription,
    FacetType,
    KrefPratice,
    Mixpoint,
    Risk,
    Role,
    Schapter,
)
from tests.authentication.factories import create_user
from tests.organizations.factories import create_organization


_blave_counter = count(1)
_boundary_counter = count(1)
_role_counter = count(1)
_schapter_counter = count(1)
_facet_description_counter = count(1)
_risk_counter = count(1)
_kref_pratice_counter = count(1)
_concrete_action_counter = count(1)
_mixpoint_counter = count(1)


def create_blave(*, organization=None, created_by_user=None, **overrides):
    """Cria uma blave para testes com dados previsiveis."""
    sequence = next(_blave_counter)
    created_by_user = created_by_user or create_user(
        username=f"blave-owner-{sequence}",
    )
    organization = organization or create_organization(created_by=created_by_user)
    data = {
        "organization": organization,
        "created_by_user": created_by_user,
        "title": f"Blave {sequence}",
    }
    data.update(overrides)
    return Blave.objects.create(**data)


def create_boundary(*, blave=None, outer_boundary=None, **overrides):
    """Cria uma boundary para testes com dados previsiveis."""
    sequence = next(_boundary_counter)
    blave = blave or create_blave()
    data = {
        "blave": blave,
        "outer_boundary": outer_boundary,
        "name": f"Boundary {sequence}",
        "description": "",
    }
    data.update(overrides)
    return Boundary.objects.create(**data)


def create_role(*, organization=None, **overrides):
    """Cria uma role para testes com dados previsiveis."""
    sequence = next(_role_counter)
    organization = organization or create_organization()
    data = {
        "organization": organization,
        "name": f"Role {sequence}",
        "type": ActorType.ROLE,
    }
    data.update(overrides)
    return Role.objects.create(**data)


def create_schapter(*, boundary=None, roles=None, **overrides):
    """Cria uma schapter para testes com dados previsiveis."""
    sequence = next(_schapter_counter)
    boundary = boundary or create_boundary()
    data = {
        "boundary": boundary,
        "name": f"Schapter {sequence}",
    }
    data.update(overrides)
    schapter = Schapter.objects.create(**data)
    if roles:
        schapter.roles.set(roles)
    return schapter


def create_facet_description(*, schapter=None, **overrides):
    """Cria uma facet description para testes com dados previsiveis."""
    sequence = next(_facet_description_counter)
    schapter = schapter or create_schapter()
    data = {
        "schapter": schapter,
        "facet": FacetType.WHAT,
        "generate_risk": False,
        "value": f"Facet value {sequence}",
        "observation": "",
    }
    data.update(overrides)
    return FacetDescription.objects.create(**data)


def create_risk(*, facet_description=None, **overrides):
    """Cria um risco para testes com dados previsiveis."""
    sequence = next(_risk_counter)
    facet_description = facet_description or create_facet_description(
        facet=FacetType.WHY,
        generate_risk=True,
    )
    data = {
        "facet_description": facet_description,
        "formated_text": f"Risk {sequence}",
        "strategic_impact": f"Strategic impact {sequence}",
        "operational_impact": f"Operational impact {sequence}",
        "tactical_impact": f"Tactical impact {sequence}",
    }
    data.update(overrides)
    return Risk.objects.create(**data)


def create_kref_pratice(*, risk=None, **overrides):
    """Cria uma pratica KREF para testes com dados previsiveis."""
    sequence = next(_kref_pratice_counter)
    risk = risk or create_risk()
    data = {
        "risk": risk,
        "pratice": f"KREF practice {sequence}",
        "references": f"Reference {sequence}",
    }
    data.update(overrides)
    return KrefPratice.objects.create(**data)


def create_concrete_action(*, kref_pratice=None, **overrides):
    """Cria uma acao concreta para testes com dados previsiveis."""
    sequence = next(_concrete_action_counter)
    kref_pratice = kref_pratice or create_kref_pratice()
    data = {
        "kref_pratice": kref_pratice,
        "description": f"Concrete action {sequence}",
    }
    data.update(overrides)
    return ConcreteAction.objects.create(**data)


def create_mixpoint(*, concrete_action=None, **overrides):
    """Cria um mixpoint para testes com dados previsiveis."""
    sequence = next(_mixpoint_counter)
    concrete_action = concrete_action or create_concrete_action()
    data = {
        "concrete_action": concrete_action,
        "description": f"Mixpoint {sequence}",
    }
    data.update(overrides)
    return Mixpoint.objects.create(**data)
