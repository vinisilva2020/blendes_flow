from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.schapter import (
    SchapterGlobalListRateThrottle,
    SchapterManagementRateThrottle,
)
from apps.blendes_flow.common.views.schapter import SchapterAPIView
from apps.blendes_flow.serializers.schapters import (
    SchapterGlobalNameSerializerV1,
    SchapterInputSerializerV1,
    SchapterOutputSerializerV1,
    SchapterPartialInputSerializerV1,
)
from apps.blendes_flow.services.schapters import (
    create_schapter_service,
    delete_schapter_service,
    get_schapter_service,
    list_global_schapter_names_service,
    list_schapters_service,
    update_schapter_service,
)


class SchapterGlobalPagination(PageNumberPagination):
    """Pagina nomes globais de schapters com limite pequeno."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class SchaptersAPIViewV1(SchapterAPIView):
    """Lista e cadastra schapters dentro de uma boundary."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [SchapterManagementRateThrottle]

    @extend_schema(
        tags=["Schapters"],
        responses={
            200: SchapterOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, boundary_id):
        schapters = list_schapters_service(
            user=request.user,
            boundary_id=boundary_id,
        )
        serializer = SchapterOutputSerializerV1(schapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Schapters"],
        request=SchapterInputSerializerV1,
        responses={
            201: SchapterOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def post(self, request, boundary_id):
        input_serializer = SchapterInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        schapter = create_schapter_service(
            user=request.user,
            boundary_id=boundary_id,
            **input_serializer.validated_data,
        )

        output_serializer = SchapterOutputSerializerV1(schapter)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class SchapterDetailAPIViewV1(SchapterAPIView):
    """Recupera, atualiza e remove uma schapter do usuario autenticado."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [SchapterManagementRateThrottle]

    @extend_schema(
        tags=["Schapters"],
        responses={
            200: SchapterOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, schapter_id):
        schapter = get_schapter_service(
            user=request.user,
            schapter_id=schapter_id,
        )
        serializer = SchapterOutputSerializerV1(schapter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Schapters"],
        request=SchapterPartialInputSerializerV1,
        responses={
            200: SchapterOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def patch(self, request, schapter_id):
        input_serializer = SchapterPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        schapter = update_schapter_service(
            user=request.user,
            schapter_id=schapter_id,
            **input_serializer.validated_data,
        )
        serializer = SchapterOutputSerializerV1(schapter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Schapters"],
        request=None,
        responses={
            204: OpenApiResponse(description="Schapter deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(self, request, schapter_id):
        delete_schapter_service(
            user=request.user,
            schapter_id=schapter_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchapterGlobalNamesAPIViewV1(SchapterAPIView):
    """Lista nomes globais de schapters para importacao."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [SchapterGlobalListRateThrottle]
    pagination_class = SchapterGlobalPagination

    @extend_schema(
        tags=["Schapters"],
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
            200: SchapterGlobalNameSerializerV1(many=True),
            401: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        names = list_global_schapter_names_service()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(names, request, view=self)
        serializer = SchapterGlobalNameSerializerV1(page, many=True)
        return paginator.get_paginated_response(serializer.data)
