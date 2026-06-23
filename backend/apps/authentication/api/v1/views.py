from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import (
    APIErrorSerializerV1,
    AuthenticationOutputSerializerV1,
    AuthenticationSessionOutputSerializerV1,
    GoogleLoginInputSerializerV1,
    LoginInputSerializerV1,
    RefreshTokenInputSerializerV1,
)
from apps.authentication.common.throttles import (
    LoginRateThrottle,
    RefreshRateThrottle,
)
from apps.authentication.common.views import AuthenticationAPIView
from apps.authentication.models import AuthenticationSession
from apps.authentication.services import (
    authenticate_google_user_service,
    authenticate_user_service,
    refresh_authentication_session_service,
    revoke_authentication_session_service,
)


class LoginAPIViewV1(AuthenticationAPIView):
    """Autentica um usuário e retorna os tokens de acesso e refresh."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=LoginInputSerializerV1,
        responses={
            200: AuthenticationOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
        auth=[],
    )
    def post(self, request):
        """Autentica um usuário e retorna os tokens de acesso e refresh."""
        input_serializer = LoginInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        tokens = authenticate_user_service(
            identifier=input_serializer.validated_data["identifier"],
            password=input_serializer.validated_data["password"],
        )
        output_serializer = AuthenticationOutputSerializerV1(tokens)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class GoogleLoginAPIViewV1(AuthenticationAPIView):
    """Autentica um usuario com uma credencial validada pelo Google."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=GoogleLoginInputSerializerV1,
        responses={
            200: AuthenticationOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
            503: APIErrorSerializerV1,
        },
        auth=[],
    )
    def post(self, request):
        """Autentica usando a credencial do Google Identity Services."""
        input_serializer = GoogleLoginInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        tokens = authenticate_google_user_service(
            credential=input_serializer.validated_data["credential"],
        )
        output_serializer = AuthenticationOutputSerializerV1(tokens)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class RefreshTokenAPIViewV1(AuthenticationAPIView):
    """Renova os tokens de acesso e refresh usando um token de refresh válido."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [RefreshRateThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=RefreshTokenInputSerializerV1,
        responses={
            200: AuthenticationOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
        auth=[],
    )
    def post(self, request):
        """Renova os tokens de acesso e refresh usando um token de refresh válido."""
        input_serializer = RefreshTokenInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        tokens = refresh_authentication_session_service(
            refresh_token=input_serializer.validated_data["refresh_token"]
        )

        output_serializer = AuthenticationOutputSerializerV1(tokens)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class LogoutAPIViewV1(AuthenticationAPIView):
    """Encerra a sessão de autenticação atual, invalidando os tokens."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        request=None,
        responses={
            204: OpenApiResponse(description="Authentication session revoked."),
            401: APIErrorSerializerV1,
        },
    )
    def post(self, request):
        """Revoga a sessão de autenticação atual do usuário."""
        revoke_authentication_session_service(
            session_id=request.auth["session_id"], user_id=request.user.pk
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthenticationSessionsAPIViewV1(AuthenticationAPIView):
    """Lista as sessões de autenticação ativas do usuário."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        responses={
            200: AuthenticationSessionOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        """Retorna as sessões de autenticação ativas do usuário."""
        sessions = AuthenticationSession.objects.filter(
            user_id=request.user.pk,
            revoked_at__isnull=True,
            expires_at__gt=timezone.now(),
        )

        serializer = AuthenticationSessionOutputSerializerV1(
            sessions,
            many=True,
            context={"current_session_id": request.auth["session_id"]},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class RevokeSessionAPIViewV1(AuthenticationAPIView):
    """Revoga uma sessão de autenticação específica do usuário."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        request=None,
        responses={
            204: OpenApiResponse(description="Authentication session revoked."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def delete(self, request, session_id):
        """Revoga a sessão de autenticação especificada pelo ID."""
        revoke_authentication_session_service(
            session_id=session_id, user_id=request.user.pk
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
