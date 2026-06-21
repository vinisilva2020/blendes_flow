from django.urls import include, path

app_name = "organizations"

urlpatterns = [
    path("v1/organizations/", include("apps.organizations.api.v1.urls")),
]
