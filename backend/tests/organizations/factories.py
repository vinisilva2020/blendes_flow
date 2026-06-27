from itertools import count

from apps.organizations.models import Organization
from tests.authentication.factories import create_user


_organization_counter = count(1)


def create_organization(*, created_by=None, **overrides):
    sequence = next(_organization_counter)
    created_by = created_by or create_user(username=f"org-owner-{sequence}")
    data = {
        "name": f"Organization {sequence}",
        "description": f"Organization {sequence} description",
        "created_by": created_by,
        "is_active": True,
    }
    data.update(overrides)
    return Organization.objects.create(**data)
