from django.urls import include, path

app_name = "blendes_v1"

urlpatterns = [
    path("", include("apps.blendes.api.v1.execution.urls")),
]
