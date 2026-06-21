import datetime
import hashlib
import secrets
import uuid
from dataclasses import dataclass

from django.conf import settings
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

# Configurações de autenticação
REFRESH_SECRET_BYTES = 48


class AuthenticationSession(models.Model):
    """
    Representa uma sessão autenticada e revogável de um usuário.


    Atributos:
    - `id`: Identificador único da autenticação (UUID).
    - `user`: Referência ao usuário autenticado.
    - `refresh_token`: Token de atualização exclusivo para esta autenticação.
    - `expires_at`: Data e hora de expiração da autenticação.
    - `revoked_at`: Data e hora em que a autenticação foi revogada (se aplicável).
    - `created_at`: Data e hora de criação da autenticação.
    - `updated_at`: Data e hora da última atualização da autenticação.

    Indices:
    - Índice composto em `user`, `revoked_at` e `expires_at` para otimizar consultas de autenticações ativas.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authentications",
    )
    refresh_token_hash = models.CharField(max_length=64, unique=True, editable=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "revoked_at", "expires_at"],
                name="user_revoked_expires_idx",
            ),
        ]

    def __str__(self):
        return f"AuthenticationSession(id={self.id}, user_id={self.user_id})"

    @property
    def is_revoked(self):
        """Indica se a autenticação foi revogada."""
        return self.revoked_at is not None

    @property
    def is_expired(self):
        """Indica se a autenticação expirou."""
        return self.expires_at is None or self.expires_at <= timezone.now()

    @property
    def is_active(self):
        """Indica se a autenticação está ativa."""
        return not self.is_revoked and not self.is_expired


class SessionJWTAuthentication(JWTAuthentication):
    """
    Classe de autenticação JWT personalizada que verifica se a sessão do usuário está ativa.

    O JWT de acesso deve possuir a claim 'session_id'. Além das validações executadas pelo SimpleJWT,
    o backend confirma que a sessão pertence ao usuário autenticado e que ainda não expirou ou foi revogada. Caso contrário, a autenticação falha.
    """

    def get_user(self, validated_token):
        """
        Retorna o usuário associado ao token validado, verificando se a sessão está ativa.

        Args:
            validated_token: Token JWT validado.
        """
        user = super().get_user(validated_token)
        session_id = validated_token.get("session_id")
        if not session_id:
            raise AuthenticationFailed(
                "The token does not contain a valid session.", code="invalid_session"
            )
        try:
            session_uuid = uuid.UUID(str(session_id))
        except (TypeError, ValueError):
            raise AuthenticationFailed(
                "The token does not contain a valid session.", code="invalid_session"
            )

        session = AuthenticationSession.objects.filter(
            id=session_uuid,
            user=user,
            revoked_at__isnull=True,
            expires_at__gt=timezone.now(),
        ).first()
        if session is None:
            raise AuthenticationFailed(
                "The authentication session was revoked, expired, or does not exist.",
                code="session_not_active",
            )

        return user


@dataclass(frozen=True)
class AuthenticationTokens:
    """Estrutura de dados para armazenar os tokens de autenticação."""

    access_token: str
    refresh_token: str
    token_type: str
    access_expires_in: int
    refresh_expires_at: datetime.datetime
    session_id: uuid.UUID

    @staticmethod
    def generate_refresh_secret():
        """Gera um segredo aleatório para o token de atualização."""
        return secrets.token_urlsafe(REFRESH_SECRET_BYTES)

    @staticmethod
    def hash_refresh_token(secret):
        """Calcula o hash SHA-256 utilizado para persistir o token de atualização."""
        return hashlib.sha256(secret.encode("utf-8")).hexdigest()

    has_refresh_token = hash_refresh_token

    @staticmethod
    def build_refresh_token(*, session_id, secret):
        """Compõe a credencial opaca com o identificador e o segredo da sessão."""
        return f"{session_id}.{secret}"

    @staticmethod
    def parse_refresh_token(refresh_token):
        """Separa e valida estruturalmente uma credencial de renovação"""

        try:
            session_id_value, secret = refresh_token.split(".", maxsplit=1)
            session_id = uuid.UUID(session_id_value)
        except (AttributeError, TypeError, ValueError):
            return None

        if not secret:
            return None

        return session_id, secret

    @staticmethod
    def issue_authentication_tokens(*, session, refresh_secret):
        """Emite os tokens de acesso e atualização para uma sessão autenticada."""
        access_token = AccessToken.for_user(session.user)
        access_token["session_id"] = str(session.id)

        return AuthenticationTokens(
            access_token=str(access_token),
            refresh_token=AuthenticationTokens.build_refresh_token(
                session_id=session.id, secret=refresh_secret
            ),
            token_type="Bearer",
            access_expires_in=int(
                settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
            ),
            refresh_expires_at=session.expires_at,
            session_id=session.id,
        )
