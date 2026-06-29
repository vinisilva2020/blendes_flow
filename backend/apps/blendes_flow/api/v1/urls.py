from django.urls import path

from apps.blendes_flow.api.v1.views.boundaries import (
    BoundariesAPIViewV1,
    BoundaryDetailAPIViewV1,
    BoundaryGlobalNamesAPIViewV1,
)
from apps.blendes_flow.api.v1.views.facet_descriptions import (
    FacetDescriptionDetailAPIViewV1,
    FacetDescriptionsAPIViewV1,
)
from apps.blendes_flow.api.v1.views.kref_pratices import (
    KrefPraticeDetailAPIViewV1,
    KrefPraticesAPIViewV1,
)
from apps.blendes_flow.api.v1.views.mixpoints import (
    MixpointDetailAPIViewV1,
    MixpointsAPIViewV1,
)
from apps.blendes_flow.api.v1.views.risks import (
    RiskDetailAPIViewV1,
    RisksAPIViewV1,
)
from apps.blendes_flow.api.v1.views.schapters import (
    SchapterDetailAPIViewV1,
    SchapterGlobalNamesAPIViewV1,
    SchaptersAPIViewV1,
)
from apps.blendes_flow.api.v1.views.blaves import (
    BlaveDetailAPIViewV1,
    BlavesAPIViewV1,
)

app_name = "blendes_flow_v1"

urlpatterns = [
    path(
        "boundaries/",
        BoundaryGlobalNamesAPIViewV1.as_view(),
        name="boundary-global-names",
    ),
    path(
        "schapters/",
        SchapterGlobalNamesAPIViewV1.as_view(),
        name="schapter-global-names",
    ),
    path(
        "organizations/<int:organization_id>/blaves/",
        BlavesAPIViewV1.as_view(),
        name="blave-list",
    ),
    path(
        "blaves/<int:blave_id>/",
        BlaveDetailAPIViewV1.as_view(),
        name="blave-detail",
    ),
    path(
        "blaves/<int:blave_id>/boundaries/",
        BoundariesAPIViewV1.as_view(),
        name="boundary-list",
    ),
    path(
        "boundaries/<int:boundary_id>/",
        BoundaryDetailAPIViewV1.as_view(),
        name="boundary-detail",
    ),
    path(
        "boundaries/<int:boundary_id>/schapters/",
        SchaptersAPIViewV1.as_view(),
        name="schapter-list",
    ),
    path(
        "schapters/<int:schapter_id>/",
        SchapterDetailAPIViewV1.as_view(),
        name="schapter-detail",
    ),
    path(
        "schapters/<int:schapter_id>/facet-descriptions/",
        FacetDescriptionsAPIViewV1.as_view(),
        name="facet-description-list",
    ),
    path(
        "facet-descriptions/<int:facet_description_id>/",
        FacetDescriptionDetailAPIViewV1.as_view(),
        name="facet-description-detail",
    ),
    path(
        "facet-descriptions/<int:facet_description_id>/risks/",
        RisksAPIViewV1.as_view(),
        name="risk-list",
    ),
    path(
        "risks/<int:risk_id>/",
        RiskDetailAPIViewV1.as_view(),
        name="risk-detail",
    ),
    path(
        "risks/<int:risk_id>/kref-pratices/",
        KrefPraticesAPIViewV1.as_view(),
        name="kref-pratice-list",
    ),
    path(
        "kref-pratices/<int:kref_pratice_id>/",
        KrefPraticeDetailAPIViewV1.as_view(),
        name="kref-pratice-detail",
    ),
    path(
        "concrete-actions/<int:concrete_action_id>/mixpoints/",
        MixpointsAPIViewV1.as_view(),
        name="mixpoint-list",
    ),
    path(
        "mixpoints/<int:mixpoint_id>/",
        MixpointDetailAPIViewV1.as_view(),
        name="mixpoint-detail",
    ),
]
