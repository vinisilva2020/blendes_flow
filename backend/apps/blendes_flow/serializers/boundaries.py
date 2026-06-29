from rest_framework import serializers

from apps.blendes_flow.models import Boundary


class BoundaryInputSerializerV1(serializers.Serializer):
    """Valida os dados usados no cadastro de uma boundary."""

    name = serializers.CharField(max_length=255, trim_whitespace=True)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
    )
    outer_boundary_id = serializers.IntegerField(required=False)
    outer_boundary_name = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )

    def validate(self, attrs):
        """Garante que apenas uma estrategia de boundary pai seja usada."""
        if attrs.get("outer_boundary_id") and attrs.get("outer_boundary_name"):
            raise serializers.ValidationError(
                {
                    "outer_boundary": (
                        "Use either outer_boundary_id or outer_boundary_name."
                    )
                }
            )
        return attrs


class BoundaryPartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de uma boundary."""

    name = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
    )
    outer_boundary_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )


class BoundaryOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma boundary com sua referencia hierarquica."""

    class Meta:
        model = Boundary
        fields = [
            "id",
            "blave",
            "outer_boundary",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class BoundaryGlobalNameSerializerV1(serializers.Serializer):
    """Serializa nomes globais de boundaries para importacao."""

    name = serializers.CharField(read_only=True)
