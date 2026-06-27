from django.urls import include, path

app_name = "blendes"

urlpatterns = [
    path("v1/", include("apps.blendes.api.v1.urls")),
]
