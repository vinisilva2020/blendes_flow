from django.urls import path

from apps.accounts.api.v1.views import AccountsAPIViewV1, CurrentAccountAPIViewV1

app_name = "accounts_v1"

urlpatterns = [
    path("", AccountsAPIViewV1.as_view(), name="account-list"),
    path("me/", CurrentAccountAPIViewV1.as_view(), name="account-me"),
]
