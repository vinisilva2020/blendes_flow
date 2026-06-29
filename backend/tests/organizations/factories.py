from itertools import count

from apps.organizations.models import Organization, OrganizationMembership, Role
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


def create_membership(*, user, organization, role=Role.OWNER):
    return OrganizationMembership.objects.create(
        user=user,
        organization=organization,
        role=role,
    )


def create_organization_with_membership(*, user, role=Role.OWNER, **overrides):
    organization = create_organization(created_by=user, **overrides)
    membership = create_membership(
        user=user,
        organization=organization,
        role=role,
    )
    return organization, membership
