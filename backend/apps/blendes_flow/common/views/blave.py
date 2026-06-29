import math

from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blendes_flow.exceptions.blaves import (
    BlaveDomainError,
    BlaveNotFoundError,
    BlaveOrganizationInactiveError,
    BlaveOrganizationNotFoundError,
)

DOMAIN_ERROR_STATUS = {
    BlaveNotFoundError: 404,
    BlaveOrganizationNotFoundError: 404,
    BlaveOrganizationInactiveError: 409,
}

PUBLIC_API_EXCEPTION_MESSAGES = {
    "authentication_required": "Authentication credentials were not provided.",
    "invalid_access_token": "The access token is invalid or has expired.",
    "permission_denied": "You do not have permission to perform this action.",
    "throttled": "Request was throttled.",
}


class BlaveAPIView(APIView):
    """Aplica o contrato publico de erros para endpoints de blaves."""

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

        if isinstance(exc, ValidationError):
            return Response(
                {
                    "error": {
                        "code": "validation_error",
                        "message": "The submitted data is invalid.",
                        "details": exc.detail,
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
