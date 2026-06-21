from django.db import models
from django.conf import settings


class Role(models.TextChoices):
    """Define os papéis disponíveis para os membros de uma organização."""

    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"


class OrganizationMembership(models.Model):
    """Representa a associação de um usuário a uma organização.

    Atributos:
    - `id`: Identificador único da associação (bigAutoField).
    - `user`: Referência ao usuário associado.
    - `organization`: Referência à organização associada.
    - `role`: Papel do usuário dentro da organização (ex: 'admin', 'member').
    - `created_at`: Data e hora de criação da associação.
    - `updated_at`: Data e hora da última atualização da associação.

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="unique_user_organization_membership",
            )
        ]

    @property
    def can_manage(self):
        return self.role in [Role.ADMIN, Role.OWNER]

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class Organization(models.Model):
    """Representa uma organização dentro do sistema.

    Atributos:
    - `id`: Identificador único da organização (UUID).
    - `name`: Nome da organização.
    - `description`: Descrição opcional da organização.
    - `created_at`: Data e hora de criação da organização.
    - `updated_at`: Data e hora da última atualização da organização.
    - `is_active`: Indica se a organização está ativa ou inativa.
    - `created_by`: Referência ao usuário que criou a organização.

    """

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
