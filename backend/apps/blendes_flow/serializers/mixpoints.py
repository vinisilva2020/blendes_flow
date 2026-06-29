from rest_framework import serializers

from apps.blendes_flow.models import Mixpoint


class MixpointItemInputSerializerV1(serializers.Serializer):
    """Valida um mixpoint aninhado do cadastro em lote."""

    description = serializers.CharField(max_length=255, trim_whitespace=True)


class MixpointInputSerializerV1(serializers.Serializer):
    """Valida o cadastro em lote de mixpoints de uma acao concreta."""

    mixpoints = MixpointItemInputSerializerV1(many=True)

    def validate_mixpoints(self, value):
        """Garante que ao menos um mixpoint seja enviado."""
        if not value:
            raise serializers.ValidationError(
                "At least one mixpoint must be submitted."
            )
        return value


class MixpointPartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de um mixpoint."""

    description = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )


class MixpointOutputSerializerV1(serializers.ModelSerializer):
    """Serializa um mixpoint vinculado a uma acao concreta."""

    class Meta:
        model = Mixpoint
        fields = [
            "id",
            "concrete_action",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
