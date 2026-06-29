from django.conf import settings
from django.db import models


class Organization(models.Model):
    """Representa uma organizacao criada por um usuario do sistema."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_organizations",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_organization_name",
            )
        ]

    def __str__(self):
        return self.name


class Role(models.TextChoices):
    OWNER = "OWNER", "Owner"
    ADMIN = "ADMIN", "Admin"
    MEMBER = "MEMBER", "Member"


class OrganizationMembership(models.Model):
    """Connects a user to an organization with a role."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"],
                name="unique_organization_membership",
            )
        ]

    @property
    def can_manage(self):
        return self.role in {Role.OWNER, Role.ADMIN}

    def __str__(self):
        return f"{self.user_id}:{self.organization_id}:{self.role}"
