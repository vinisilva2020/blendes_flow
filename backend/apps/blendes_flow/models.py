from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FacetType(models.TextChoices):
    WHAT = "WHAT", "What"
    WHY = "WHY", "Why"
    WHEN = "WHEN", "When"
    WHO = "WHO", "Who"
    WITH = "WITH", "With"
    WHEREBY = "WHEREBY", "Whereby"
    IN = "IN", "in"
    OUT = "OUT", "Out"


class Movement(models.TextChoices):
    BOUNDGROUND = "BOUNDGROUND", "Boundground"
    LABOR = "LABOR", "Labor"
    ECHO = "ECHO", "Echo"
    NOISECATCH = "NOISECATCH", "Noisecatch"
    DRAWBRIDGE = "DRAWBRIDGE", "Drawbridge"
    ENHANCE = "ENHANCE", "Enhance"
    SIGHTLINE = "SIGHTLINE", "Sightline"


class MovementStatus(models.TextChoices):
    LOCKED = "LOCKED", "Bloqueado"
    ACTIVE = "ACTIVE", "Ativo"
    COMPLETED = "COMPLETED", "Concluido"
    INVALIDATED = "INVALIDATED", "Invalidado"


class BlaveStatus(models.TextChoices):
    DRAFT = "DRAFT", "Rascunho"
    IN_PROGRESS = "IN_PROGRESS", "Em andamento"
    COMPLETED = "COMPLETED", "Concluida"
    ARCHIVED = "ARCHIVED", "Arquivada"


class ActorType(models.TextChoices):
    ROLE = "ROLE", "Role"
    GROUP = "GROUP", "Group"


class Blave(TimeStampedModel):
    """
    Representa um ciclo de execução do método blendes, define o direcionamento que o blendes vai navegar

    Atributos:
    organization: representa a organização que a blave está rodando.
    created_by_user: representa o usuário que criou a blave.
    title: representa o titulo e objetivo da blave.
    status: representa o status da blave.
    current_movement: representa o movimento atual que a blave está
    version: a versão da blave
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="blaves",
    )
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_blaves",
    )
    title = models.CharField(max_length=255)
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

    class Meta:
        db_table = "blave"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "current_movement"]),
        ]

    def __str__(self):
        return self.title


class BlaveMovements(models.Model):
    """
    Representa os movimentos de uma blave.
    essa entidade é criada automaticamente com os movimentos do blendes conforme uma blave é iniciada.

    atributos:
    blave: relação com a blave pai.
    movement: representa um movimento fixo do blendes.
    status: representa a situação atual do movimento.
    completed_at: representa a data que o movimento foi finalizado
    reopen_at: representa a data que o movimento foi aberto novamente
    """

    blave = models.ForeignKey(
        Blave,
        on_delete=models.CASCADE,
        related_name="movement_statuses",
    )
    movement = models.CharField(max_length=30, choices=Movement.choices)
    status = models.CharField(
        max_length=30,
        choices=MovementStatus.choices,
        default=MovementStatus.LOCKED,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    reopen_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "blave_movements"
        ordering = ["blave", "movement"]
        constraints = [
            models.UniqueConstraint(
                fields=["blave", "movement"],
                name="uq_blave_movement_status",
            )
        ]

    def __str__(self):
        return f"{self.blave} - {self.movement}: {self.status}"


class Boundary(TimeStampedModel):
    """
    Representa a área delimitada em que uma análise é realizada dentro da blave.

    atributos:
    blave: representa a blave que a boundary foi analisada.
    outer_boundary: representa a boundary contextual ou pai (superior a filha)
    name: representa o nome do dominio
    description: representa uma descrição da boundary
    """

    blave = models.ForeignKey(
        Blave, on_delete=models.CASCADE, related_name="boundaries"
    )
    outer_boundary = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inner_boundaries",
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "boundaries"
        ordering = ["name", "created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "blave"], name="uq_boundary_blave_name"
            )
        ]


class Schapter(TimeStampedModel):
    """
    Representa uma unidade de trabalho executada dentro de um limite funcional.

    atributos:
    boundary: lugar onde o trabalho é executado.
    name: nome do trabalho que é realizado
    roles: multiplas roles que executam esse trabalho
    """

    boundary = models.ForeignKey(
        Boundary, on_delete=models.CASCADE, related_name="schapters"
    )
    name = models.CharField(max_length=255, db_index=True)
    roles = models.ManyToManyField(
        "Role",
        through="RoleExecutionSchapter",
        related_name="schapters",
        blank=True,
    )

    class Meta:
        db_table = "schapters"
        ordering = ["name", "created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["name", "boundary"],
                name="uq_schapter_name",
            )
        ]


class Role(TimeStampedModel):
    """
    Representa um cargo/papel que existe dentro da organização

    atributos:
    organization: relação para a organização que possui aquele papel
    name: nome do papel
    type: tipo do papel, serve para indicar se é executado por um role individual ou um grupo
    """

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="roles"
    )
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=20, choices=ActorType, default=ActorType.ROLE)

    class Meta:
        db_table = "roles"
        ordering = ["name", "created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["name", "organization"],
                name="uq_role_organization_name",
            )
        ]


class RoleExecutionSchapter(models.Model):
    """
    Representa a execução de uma schapter por uma determinada role
    serve como uma tabela intermediaria entre Role e Schapter

    atributos:
    schapter: trabalho executado
    role: cargo ou papel que executa
    """

    schapter = models.ForeignKey(
        Schapter,
        on_delete=models.CASCADE,
        related_name="role_executions",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="schapter_executions",
    )

    class Meta:
        db_table = "role_execution_schapter"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "schapter"],
                name="uq_role_execution_schapter",
            )
        ]


class FacetDescription(TimeStampedModel):
    """
    Representa a descrição de uma faceta para um determinado trabalho
    - o movimento echo só é validado quando existem facetDescriptions para cada faceta do blendes (modelo 6WIO)
    - faceta what não gera risco, ela apenas é descritiva.
    atributos:
    schapter: relação para o trabalho executado
    facet: faceta analisada (pertence ao modelo 6WIO)
    generate_risk: indica se a faceta pode gerar riscos (no blendes a faceta WHAT é apenas descritiva, não gera risco)
    value: descrição da faceta.
    observation: observação da faceta.
    """

    schapter = models.ForeignKey(
        Schapter, on_delete=models.CASCADE, related_name="facet_descriptions"
    )
    facet = models.CharField(
        max_length=8, choices=FacetType, default=FacetType.WHAT, db_index=True
    )
    generate_risk = models.BooleanField(default=True)
    value = models.CharField(max_length=255)
    observation = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "facet_descriptions"
        constraints = [
            models.UniqueConstraint(
                fields=["schapter", "facet"], name="uq_schapter_facet"
            )
        ]


class Risk(TimeStampedModel):
    """
    Representa um risco que determinda descrição de facet pode gerar, cada risco possui impacto operacional, estrategico e tatico
    - priotity_position: só pode ser preenchida na fase drawbridge da blave
    - um risco não pode ser gerado de uma faceta WHAT pois ela é apenas descritiva
    atributos:
    facet_description: relação com a descrição de uma faceta
    formated_text: texto formatado dentro do padrão de escrita de riscos do blendes
    strategic_impact: impacto na camada estrategica
    operational_impact: impacto na camada estrategica
    tactical_impact: impacto na camada tatica
    priority_position: posição do risco em relação a descrição das facetas de uma blave
    """

    facet_description = models.ForeignKey(
        FacetDescription, on_delete=models.CASCADE, related_name="risks"
    )
    formated_text = models.CharField(max_length=255)
    strategic_impact = models.CharField(max_length=255)
    operational_impact = models.CharField(max_length=255)
    tactical_impact = models.CharField(max_length=255)
    priority_position = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )

    class Meta:
        db_table = "risks"
        ordering = ["created_at", "priority_position"]
        constraints = [
            models.UniqueConstraint(
                fields=["facet_description", "priority_position"],
                name="uq_risk_priority_per_facet_description",
            )
        ]


class KrefPratice(TimeStampedModel):
    """
    Representa uma prática para tratar determinado risco

    atributos:
    risk: relacionamento para o risco tratado
    pratice: descrição da prática
    references: referências usadas para a prática
    """

    risk = models.ForeignKey(
        Risk, on_delete=models.CASCADE, related_name="kref_pratices"
    )

    pratice = models.CharField(max_length=255, db_index=True)
    references = models.CharField(max_length=255)

    class Meta:
        db_table = "kref_pratices"
        ordering = ["created_at", "pratice"]


class ConcreteAction(TimeStampedModel):
    """
    representa uma ação concreta para apoiar uma kref_pratice

    atributos:
    kref_pratice: relação para prática
    description: descrição da ação concreta
    """

    kref_pratice = models.OneToOneField(
        KrefPratice, on_delete=models.CASCADE, related_name="concrete_action"
    )
    description = models.CharField()

    class Meta:
        db_table = "concrete_actions"
        ordering = ["created_at"]


class Mixpoint(TimeStampedModel):
    """
    Representa um ponto de mistura ligado a uma acao concreta.

    atributos:
    concrete_action: acao concreta que recebe os pontos de mistura
    description: descricao do ponto de mistura
    """

    concrete_action = models.ForeignKey(
        ConcreteAction, on_delete=models.CASCADE, related_name="mixpoints"
    )
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "mixpoints"
        ordering = ["created_at"]
