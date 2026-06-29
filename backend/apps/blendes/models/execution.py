"""Entidades que representam a execução do método blendes, responsaveis por indicar movimento e instância atual do método"""

import uuid

from django.conf import settings
from django.db import models


class Movement(models.TextChoices):
    """
    Representa os movimentos do blendes
    """

    BOUNDGROUND = "BOUNDGROUND", "Boundground"
    LABOR = "LABOR", "Labor"
    ECHO = "ECHO", "Echo"
    NOISECATCH = "NOISECATCH", "Noisecatch"
    DRAWBRIDGE = "DRAWBRIDGE", "Drawbridge"
    ENHANCE = "ENHANCE", "Enhance"
    SIGHTLINE = "SIGHTLINE", "Sightline"


class MovementStatus(models.TextChoices):
    """
    Representa o status de um movimento
    """

    LOCKED = "LOCKED", "Bloqueado"
    ACTIVE = "ACTIVE", "Ativo"
    COMPLETED = "COMPLETED", "Concluido"
    INVALIDATED = "INVALIDATED", "Invalidado"


class BlaveStatus(models.TextChoices):
    """
    Representa o status de uma blave
    """

    DRAFT = "DRAFT", "Rascunho"
    IN_PROGRESS = "IN_PROGRESS", "Em andamento"
    COMPLETED = "COMPLETED", "Concluida"
    ARCHIVED = "ARCHIVED", "Arquivada"


class Blave(models.Model):
    """
    Representa uma execução do blendes

    atributos:

    """

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="blaves"
    )

    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_blaves",
    )

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30,
        choices=BlaveStatus.choices,
        default=BlaveStatus.DRAFT,
    )
    current_movement = models.CharField(
        max_length=30,
        choices=Movement.choices,
        default=Movement.BOUNDGROUND,
    )

    version_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blaves"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "current_movement"]),
        ]

    def __str__(self):
        return self.title


class BlaveMovementStatus(models.Model):
    """
    Representa os status de cada movimento da blave
    """

    blave = models.ForeignKey(
        Blave, on_delete=models.CASCADE, related_name="movement_statuses"
    )
    movement = models.CharField(max_length=30, choices=Movement.choices)
    status = models.CharField(
        max_length=30,
        choices=MovementStatus.choices,
        default=MovementStatus.LOCKED,
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "blave_movement_status"
        ordering = ["blave", "movement"]
        constraints = [
            models.UniqueConstraint(
                fields=["blave", "movement"],
                name="uq_blave_movement_status",
            )
        ]

    def __str__(self):
        return f"{self.blave} - {self.movement}: {self.status}"


class BlaveRevision(models.Model):
    """
    Representa uma revisão da blave (versões geradas)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blave = models.ForeignKey(
        Blave,
        on_delete=models.CASCADE,
        related_name="revisions",
    )
    revision_number = models.PositiveIntegerField()
    movement = models.CharField(max_length=30, choices=Movement.choices)
    snapshot_json = models.JSONField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_blave_revisions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "blave_revision"
        ordering = ["blave", "-revision_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["blave", "revision_number"],
                name="uq_blave_revision_number",
            )
        ]

    def __str__(self):
        return f"{self.blave} v{self.revision_number}"
