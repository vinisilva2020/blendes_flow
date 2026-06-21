from django.conf import settings
from django.http import HttpResponse


class CorsMiddleware:
    """Adds CORS headers for explicitly allowed browser origins."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        is_preflight = (
            request.method == "OPTIONS"
            and "Access-Control-Request-Method" in request.headers
        )

        if is_preflight and self._is_allowed_origin(origin):
            response = HttpResponse(status=200)
        else:
            response = self.get_response(request)

        if self._is_allowed_origin(origin):
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = self._append_vary_header(
                response.get("Vary", ""),
                "Origin",
            )

            if getattr(settings, "CORS_ALLOW_CREDENTIALS", False):
                response["Access-Control-Allow-Credentials"] = "true"

            if is_preflight:
                response["Access-Control-Allow-Methods"] = ", ".join(
                    settings.CORS_ALLOW_METHODS
                )
                response["Access-Control-Allow-Headers"] = ", ".join(
                    settings.CORS_ALLOW_HEADERS
                )
                response["Access-Control-Max-Age"] = str(settings.CORS_MAX_AGE)

        return response

    @staticmethod
    def _is_allowed_origin(origin):
        return bool(origin and origin in settings.CORS_ALLOWED_ORIGINS)

    @staticmethod
    def _append_vary_header(current_value, next_value):
        values = [value.strip() for value in current_value.split(",") if value.strip()]

        if next_value not in values:
            values.append(next_value)

        return ", ".join(values)
