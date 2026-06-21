from django.urls import path

from apps.organizations.api.v1.views import (
    OrganizationDetailAPIViewV1,
    OrganizationsAPIViewV1,
)

app_name = "organizations_v1"

urlpatterns = [
    path("", OrganizationsAPIViewV1.as_view(), name="organization-list"),
    path(
        "<int:organization_id>/",
        OrganizationDetailAPIViewV1.as_view(),
        name="organization-detail",
    ),
]
