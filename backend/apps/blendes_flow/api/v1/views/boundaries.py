from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.boundary import (
    BoundaryGlobalListRateThrottle,
    BoundaryManagementRateThrottle,
)
from apps.blendes_flow.common.views.boundary import BoundaryAPIView
from apps.blendes_flow.serializers.boundaries import (
    BoundaryGlobalNameSerializerV1,
    BoundaryInputSerializerV1,
    BoundaryOutputSerializerV1,
    BoundaryPartialInputSerializerV1,
)
from apps.blendes_flow.services.boundaries import (
    create_boundary_service,
    delete_boundary_service,
    get_boundary_service,
    list_boundaries_service,
    list_global_boundary_names_service,
    update_boundary_service,
)


class BoundaryGlobalPagination(PageNumberPagination):
    """Pagina nomes globais de boundaries com limite pequeno."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class BoundariesAPIViewV1(BoundaryAPIView):
    """Lista e cadastra boundaries dentro de uma blave."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [BoundaryManagementRateThrottle]

    @extend_schema(
        tags=["Boundaries"],
        responses={
            200: BoundaryOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, blave_id):
        boundaries = list_boundaries_service(
            user=request.user,
            blave_id=blave_id,
        )
        serializer = BoundaryOutputSerializerV1(boundaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Boundaries"],
        request=BoundaryInputSerializerV1,
        responses={
            201: BoundaryOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def post(self, request, blave_id):
        input_serializer = BoundaryInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        boundary = create_boundary_service(
            user=request.user,
            blave_id=blave_id,
            **input_serializer.validated_data,
        )

        output_serializer = BoundaryOutputSerializerV1(boundary)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BoundaryDetailAPIViewV1(BoundaryAPIView):
    """Recupera, atualiza e remove uma boundary do usuario autenticado."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [BoundaryManagementRateThrottle]

    @extend_schema(
        tags=["Boundaries"],
        responses={
            200: BoundaryOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, boundary_id):
        boundary = get_boundary_service(
            user=request.user,
            boundary_id=boundary_id,
        )
        serializer = BoundaryOutputSerializerV1(boundary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Boundaries"],
        request=BoundaryPartialInputSerializerV1,
        responses={
            200: BoundaryOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def patch(self, request, boundary_id):
        input_serializer = BoundaryPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        boundary = update_boundary_service(
            user=request.user,
            boundary_id=boundary_id,
            **input_serializer.validated_data,
        )
        serializer = BoundaryOutputSerializerV1(boundary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Boundaries"],
        request=None,
        responses={
            204: OpenApiResponse(description="Boundary deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(self, request, boundary_id):
        delete_boundary_service(
            user=request.user,
            boundary_id=boundary_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoundaryGlobalNamesAPIViewV1(BoundaryAPIView):
    """Lista nomes globais de boundaries para importacao."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [BoundaryGlobalListRateThrottle]
    pagination_class = BoundaryGlobalPagination

    @extend_schema(
        tags=["Boundaries"],
        parameters=[
            OpenApiParameter(
                name="page",
                description="Numero da pagina.",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description="Quantidade por pagina, limitada a 10.",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: BoundaryGlobalNameSerializerV1(many=True),
            401: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        names = list_global_boundary_names_service()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(names, request, view=self)
        serializer = BoundaryGlobalNameSerializerV1(page, many=True)
        return paginator.get_paginated_response(serializer.data)
