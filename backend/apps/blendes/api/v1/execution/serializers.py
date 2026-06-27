from rest_framework import serializers

from apps.blendes.models.execution import (
    Blave,
    BlaveMovementStatus,
    BlaveStatus,
    Movement,
)


class BlaveInputSerializerV1(serializers.Serializer):
    """Valida os dados necessários para cadastrar uma blave."""

    organization_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=255, trim_whitespace=True)
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )


class BlaveOrganizationQuerySerializerV1(serializers.Serializer):
    """Valida a organização selecionada pela interface do usuário."""

    organization_id = serializers.IntegerField(min_value=1)


class BlavePartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos para alterar uma blave."""

    title = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    status = serializers.ChoiceField(
        choices=BlaveStatus.choices,
        required=False,
    )
    current_movement = serializers.ChoiceField(
        choices=Movement.choices,
        required=False,
    )


class BlaveMovementStatusOutputSerializerV1(serializers.ModelSerializer):
    """Serializa o status dos movimentos associados a uma blave."""

    class Meta:
        model = BlaveMovementStatus
        fields = [
            "movement",
            "status",
            "completed_at",
        ]


class BlaveOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma blave para consumo da API."""

    organization_id = serializers.IntegerField(read_only=True)
    created_by_user_id = serializers.IntegerField(read_only=True)
    movement_statuses = BlaveMovementStatusOutputSerializerV1(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Blave
        fields = [
            "id",
            "organization_id",
            "created_by_user_id",
            "title",
            "description",
            "status",
            "current_movement",
            "version_number",
            "movement_statuses",
            "created_at",
            "updated_at",
        ]
