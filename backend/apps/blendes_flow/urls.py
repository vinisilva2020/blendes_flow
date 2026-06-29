from django.urls import include, path

app_name = "blendes_flow"

urlpatterns = [
    path("v1/", include("apps.blendes_flow.api.v1.urls")),
]
