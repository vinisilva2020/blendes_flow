from itertools import count

from apps.blendes.models.execution import Blave
from tests.authentication.factories import create_user
from tests.organizations.factories import create_organization


_blave_counter = count(1)


def create_blave(*, organization=None, created_by_user=None, **overrides):
    """Cria uma blave para testes sem preparar movimentos automaticamente."""
    sequence = next(_blave_counter)
    created_by_user = created_by_user or create_user(
        username=f"blave-owner-{sequence}"
    )
    organization = organization or create_organization(created_by=created_by_user)
    data = {
        "organization": organization,
        "created_by_user": created_by_user,
        "title": f"Blave {sequence}",
        "description": f"Blave {sequence} description",
    }
    data.update(overrides)
    return Blave.objects.create(**data)
