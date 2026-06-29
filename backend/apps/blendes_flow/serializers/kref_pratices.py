from rest_framework import serializers

from apps.blendes_flow.models import KrefPratice


class KrefPraticeItemInputSerializerV1(serializers.Serializer):
    """Valida uma pratica KREF aninhada do cadastro unificado."""

    pratice = serializers.CharField(max_length=255, trim_whitespace=True)
    references = serializers.CharField(max_length=255, trim_whitespace=True)


class KrefPraticeInputSerializerV1(serializers.Serializer):
    """Valida o cadastro unificado de praticas KREF de um risco."""

    kref_pratices = KrefPraticeItemInputSerializerV1(many=True)

    def validate_kref_pratices(self, value):
        """Garante que ao menos uma pratica KREF seja enviada."""
        if not value:
            raise serializers.ValidationError(
                "At least one KREF practice must be submitted."
            )
        return value


class KrefPraticePartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de uma pratica KREF."""

    pratice = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    references = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )


class KrefPraticeOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma pratica KREF vinculada a um risco."""

    class Meta:
        model = KrefPratice
        fields = [
            "id",
            "risk",
            "pratice",
            "references",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
