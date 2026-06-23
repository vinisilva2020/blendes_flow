from django.urls import path

from apps.authentication.api.v1.views import (
    AuthenticationSessionsAPIViewV1,
    GoogleLoginAPIViewV1,
    LoginAPIViewV1,
    LogoutAPIViewV1,
    RefreshTokenAPIViewV1,
    RevokeSessionAPIViewV1,
)

app_name = "authentication_tests"

urlpatterns = [
    path("api/v1/auth/login/", LoginAPIViewV1.as_view(), name="login"),
    path("api/v1/auth/google/", GoogleLoginAPIViewV1.as_view(), name="google-login"),
    path("api/v1/auth/refresh/", RefreshTokenAPIViewV1.as_view(), name="refresh"),
    path("api/v1/auth/logout/", LogoutAPIViewV1.as_view(), name="logout"),
    path(
        "api/v1/auth/sessions/",
        AuthenticationSessionsAPIViewV1.as_view(),
        name="session-list",
    ),
    path(
        "api/v1/auth/sessions/<uuid:session_id>/",
        RevokeSessionAPIViewV1.as_view(),
        name="session-revoke",
    ),
]
