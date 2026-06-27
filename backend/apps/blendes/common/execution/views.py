import math

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blendes.exceptions.execution import (
    BlaveDomainError,
    BlaveMovementSetupError,
    BlaveNotFoundError,
)
from apps.organizations import access as organization_access

DOMAIN_ERROR_STATUS = {
    BlaveNotFoundError: 404,
    BlaveMovementSetupError: 409,
}

PUBLIC_API_EXCEPTION_MESSAGES = {
    "authentication_required": "Credenciais de autenticação não foram enviadas.",
    "invalid_access_token": "O token de acesso é inválido ou expirou.",
    "permission_denied": "Você não possui permissão para executar esta ação.",
    "throttled": "A requisição foi limitada temporariamente.",
}


class BlaveAPIView(APIView):
    """Aplica o contrato público de erros para endpoints de execução de blaves."""

    def handle_exception(self, exc):
        if isinstance(exc, BlaveDomainError):
            return Response(
                {
                    "error": {
                        "code": exc.code,
                        "message": exc.message,
                        "details": None,
                    }
                },
                status=DOMAIN_ERROR_STATUS.get(type(exc), 400),
            )

        if isinstance(exc, organization_access.OrganizationDomainError):
            return Response(
                {
                    "error": {
                        "code": exc.code,
                        "message": exc.message,
                        "details": None,
                    }
                },
                status=organization_access.get_organization_error_status(exc),
            )

        if isinstance(exc, (DjangoValidationError, ValidationError)):
            details = getattr(exc, "detail", None)
            if details is None:
                details = getattr(exc, "message_dict", None)
            if details is None:
                details = getattr(exc, "messages", None)

            return Response(
                {
                    "error": {
                        "code": "validation_error",
                        "message": "Os dados enviados são inválidos.",
                        "details": details,
                    }
                },
                status=400,
            )

        if isinstance(exc, AuthenticationFailed):
            exc.auth_header = self.get_authenticate_header(self.request)
            return self._api_exception_response(
                exc=exc,
                code="invalid_access_token",
            )

        if isinstance(exc, NotAuthenticated):
            exc.auth_header = self.get_authenticate_header(self.request)
            return self._api_exception_response(
                exc=exc,
                code="authentication_required",
            )

        if isinstance(exc, PermissionDenied):
            return self._api_exception_response(
                exc=exc,
                code="permission_denied",
            )

        if isinstance(exc, APIException):
            return self._api_exception_response(
                exc=exc,
                code=getattr(exc, "default_code", "api_error"),
            )

        return super().handle_exception(exc)

    @staticmethod
    def _api_exception_response(*, exc, code):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = str(math.ceil(exc.wait))

        return Response(
            {
                "error": {
                    "code": code,
                    "message": PUBLIC_API_EXCEPTION_MESSAGES.get(
                        code,
                        str(exc.detail),
                    ),
                    "details": None,
                }
            },
            status=exc.status_code,
            headers=headers,
        )
