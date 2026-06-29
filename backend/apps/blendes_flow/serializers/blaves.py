from rest_framework import serializers

from apps.blendes_flow.models import Blave, BlaveMovements


class BlaveInputSerializerV1(serializers.Serializer):
    """Valida os dados usados no cadastro de uma blave."""

    title = serializers.CharField(max_length=255, trim_whitespace=True)


class BlavePartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de uma blave."""

    title = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )


class BlaveMovementOutputSerializerV1(serializers.ModelSerializer):
    """Serializa o estado de um movimento da blave."""

    class Meta:
        model = BlaveMovements
        fields = [
            "id",
            "movement",
            "status",
            "completed_at",
            "reopen_at",
        ]


class BlaveOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma blave com seus movimentos de navegacao."""

    movements = BlaveMovementOutputSerializerV1(
        source="movement_statuses",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Blave
        fields = [
            "id",
            "organization",
            "created_by_user",
            "title",
            "status",
            "current_movement",
            "version_number",
            "movements",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
