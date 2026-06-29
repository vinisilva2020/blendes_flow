from rest_framework import serializers

from apps.blendes_flow.models import FacetDescription, FacetType


class FacetDescriptionItemInputSerializerV1(serializers.Serializer):
    """Valida uma faceta aninhada do cadastro unificado."""

    facet = serializers.ChoiceField(choices=FacetType.choices)
    generate_risk = serializers.BooleanField(required=False, default=True)
    value = serializers.CharField(max_length=255, trim_whitespace=True)
    observation = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )


class FacetDescriptionInputSerializerV1(serializers.Serializer):
    """Valida o cadastro unificado de facet descriptions de uma schapter."""

    facets = FacetDescriptionItemInputSerializerV1(many=True)

    def validate_facets(self, value):
        """Garante que todas as facetas sejam enviadas uma unica vez."""
        expected_facets = set(FacetType.values)
        submitted_facets = [item["facet"] for item in value]

        if len(submitted_facets) != len(set(submitted_facets)):
            raise serializers.ValidationError("Facet names must be unique.")

        missing_facets = expected_facets - set(submitted_facets)
        unexpected_facets = set(submitted_facets) - expected_facets
        if missing_facets or unexpected_facets:
            raise serializers.ValidationError(
                "All facet types must be submitted exactly once."
            )

        return value


class FacetDescriptionPartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de uma faceta."""

    generate_risk = serializers.BooleanField(required=False)
    value = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    observation = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )


class FacetDescriptionOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma facet description vinculada a uma schapter."""

    class Meta:
        model = FacetDescription
        fields = [
            "id",
            "schapter",
            "facet",
            "generate_risk",
            "value",
            "observation",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
