from django.urls import include, path

app_name = "authentication"

urlpatterns = [
    path("v1/authentication/", include("apps.authentication.api.v1.urls")),
]
