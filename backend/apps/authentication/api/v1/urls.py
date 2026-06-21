from django.urls import path

from apps.authentication.api.v1.views import (
    AuthenticationSessionsAPIViewV1,
    LoginAPIViewV1,
    LogoutAPIViewV1,
    RefreshTokenAPIViewV1,
    RevokeSessionAPIViewV1,
)

app_name = "authentication_tests"

urlpatterns = [
    path("login/", LoginAPIViewV1.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIViewV1.as_view(), name="refresh"),
    path("logout/", LogoutAPIViewV1.as_view(), name="logout"),
    path(
        "sessions/",
        AuthenticationSessionsAPIViewV1.as_view(),
        name="session-list",
    ),
    path(
        "sessions/<uuid:session_id>/",
        RevokeSessionAPIViewV1.as_view(),
        name="session-revoke",
    ),
]
