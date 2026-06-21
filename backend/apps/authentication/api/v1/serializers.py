from rest_framework import serializers

from apps.authentication.models import AuthenticationSession


class LoginInputSerializerV1(serializers.Serializer):
    """Valida o identificador e a senha usados para autenticação."""

    identifier = serializers.CharField(
        max_length=254,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
    )


class RefreshTokenInputSerializerV1(serializers.Serializer):
    """Valida o token de refresh usado para obter um novo access token."""

    refresh_token = serializers.CharField(
        max_length=256,
        trim_whitespace=False,
        write_only=True,
    )


class AuthenticationOutputSerializerV1(serializers.Serializer):
    """Serializa os dados de autenticação para a resposta da API."""

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    access_expires_in = serializers.IntegerField(read_only=True)
    refresh_expires_at = serializers.DateTimeField(read_only=True)
    session_id = serializers.UUIDField(read_only=True)


class AuthenticationSessionOutputSerializerV1(serializers.ModelSerializer):
    """Serializa os dados de uma sessão de autenticação ativa."""

    is_current = serializers.SerializerMethodField()

    class Meta:
        model = AuthenticationSession
        fields = [
            "id",
            "is_current",
            "last_used_at",
            "created_at",
            "expires_at",
        ]

    def get_is_current(self, obj):
        """Indica se esta sessão é a sessão atual do usuário."""
        return str(obj.id) == self.context.get("current_session_id")
