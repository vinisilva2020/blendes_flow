from rest_framework import serializers

from apps.blendes_flow.models import Risk


class RiskItemInputSerializerV1(serializers.Serializer):
    """Valida um risco aninhado do cadastro unificado."""

    formated_text = serializers.CharField(max_length=255, trim_whitespace=True)
    strategic_impact = serializers.CharField(max_length=255, trim_whitespace=True)
    operational_impact = serializers.CharField(max_length=255, trim_whitespace=True)
    tactical_impact = serializers.CharField(max_length=255, trim_whitespace=True)


class RiskInputSerializerV1(serializers.Serializer):
    """Valida o cadastro unificado de riscos de uma facet description."""

    risks = RiskItemInputSerializerV1(many=True)

    def validate_risks(self, value):
        """Garante que ao menos um risco seja enviado."""
        if not value:
            raise serializers.ValidationError("At least one risk must be submitted.")
        return value


class RiskPartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de um risco."""

    formated_text = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    strategic_impact = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    operational_impact = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    tactical_impact = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )


class RiskOutputSerializerV1(serializers.ModelSerializer):
    """Serializa um risco vinculado a uma facet description."""

    class Meta:
        model = Risk
        fields = [
            "id",
            "facet_description",
            "formated_text",
            "strategic_impact",
            "operational_impact",
            "tactical_impact",
            "priority_position",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
