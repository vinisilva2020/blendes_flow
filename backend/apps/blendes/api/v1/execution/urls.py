from django.urls import path

from apps.blendes.api.v1.execution.views import (
    BlaveDetailAPIViewV1,
    BlavesAPIViewV1,
)

app_name = "blendes_execution_v1"

urlpatterns = [
    path("blaves/", BlavesAPIViewV1.as_view(), name="blave-list"),
    path(
        "blaves/<int:blave_id>/",
        BlaveDetailAPIViewV1.as_view(),
        name="blave-detail",
    ),
]
