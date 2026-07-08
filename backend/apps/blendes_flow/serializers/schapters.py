from rest_framework import serializers

from apps.blendes_flow.models import ActorType, Role, Schapter, SuggestedSchapter


class SuggestedSchapterOutputSerializerV1(serializers.ModelSerializer):
    """Serializa sugestoes de schapters gerenciadas pelo software."""

    class Meta:
        model = SuggestedSchapter
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class SchapterRoleInputSerializerV1(serializers.Serializer):
    """Valida a role aninhada usada no cadastro de schapters."""

    name = serializers.CharField(max_length=255, trim_whitespace=True)
    type = serializers.ChoiceField(
        choices=ActorType.choices,
        default=ActorType.ROLE,
    )


class SchapterInputSerializerV1(serializers.Serializer):
    """Valida os dados usados no cadastro unificado de uma schapter."""

    name = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    suggested_schapter_id = serializers.IntegerField(required=False)
    roles = SchapterRoleInputSerializerV1(many=True)

    def validate(self, attrs):
        """Garante nome proprio ou uma sugestao para preencher o cadastro."""
        if not attrs.get("name") and not attrs.get("suggested_schapter_id"):
            raise serializers.ValidationError(
                {
                    "name": (
                        "This field is required when suggested_schapter_id "
                        "is not provided."
                    )
                }
            )
        return attrs

    def validate_roles(self, value):
        """Garante que a requisicao nao envie roles duplicadas."""
        seen = set()
        for role in value:
            role_key = role["name"].casefold()
            if role_key in seen:
                raise serializers.ValidationError("Role names must be unique.")
            seen.add(role_key)
        return value


class SchapterPartialInputSerializerV1(serializers.Serializer):
    """Valida os dados permitidos na atualizacao parcial de uma schapter."""

    name = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    suggested_schapter_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    roles = SchapterRoleInputSerializerV1(many=True, required=False)

    def validate_roles(self, value):
        """Garante que a requisicao nao envie roles duplicadas."""
        seen = set()
        for role in value:
            role_key = role["name"].casefold()
            if role_key in seen:
                raise serializers.ValidationError("Role names must be unique.")
            seen.add(role_key)
        return value


class SchapterRoleOutputSerializerV1(serializers.ModelSerializer):
    """Serializa roles que executam uma schapter."""

    class Meta:
        model = Role
        fields = ["id", "name", "type"]
        read_only_fields = fields


class SchapterOutputSerializerV1(serializers.ModelSerializer):
    """Serializa uma schapter com suas roles de execucao."""

    roles = SchapterRoleOutputSerializerV1(many=True, read_only=True)
    suggested_schapter = SuggestedSchapterOutputSerializerV1(read_only=True)

    class Meta:
        model = Schapter
        fields = [
            "id",
            "boundary",
            "suggested_schapter",
            "name",
            "roles",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class SchapterGlobalNameSerializerV1(serializers.Serializer):
    """Serializa nomes globais de schapters para importacao."""

    name = serializers.CharField(read_only=True)
