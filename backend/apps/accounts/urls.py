from django.urls import include, path

app_name = "accounts"

urlpatterns = [
    path("v1/accounts/", include("apps.accounts.api.v1.urls")),
]
