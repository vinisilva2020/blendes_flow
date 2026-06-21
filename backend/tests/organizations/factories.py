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


def create_membership(*, user=None, organization=None, role=Role.MEMBER):
    user = user or create_user()
    organization = organization or create_organization(created_by=user)
    return OrganizationMembership.objects.create(
        user=user,
        organization=organization,
        role=role,
    )


def create_organization_with_membership(
    *,
    user=None,
    role=Role.OWNER,
    **organization_overrides,
):
    user = user or create_user()
    organization = create_organization(created_by=user, **organization_overrides)
    membership = create_membership(
        user=user,
        organization=organization,
        role=role,
    )
    return organization, membership
