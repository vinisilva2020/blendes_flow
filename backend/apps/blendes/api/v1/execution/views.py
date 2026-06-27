from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes.api.v1.execution.serializers import (
    BlaveInputSerializerV1,
    BlaveOrganizationQuerySerializerV1,
    BlaveOutputSerializerV1,
    BlavePartialInputSerializerV1,
)
from apps.blendes.common.execution.views import BlaveAPIView
from apps.blendes.services.execution import (
    create_blave_service,
    delete_blave_service,
    get_blave_service,
    list_blaves_service,
    update_blave_service,
)


class BlavesAPIViewV1(BlaveAPIView):
    """Lista e cadastra blaves no contexto da organização selecionada."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Blaves"],
        parameters=[
            OpenApiParameter(
                name="organization_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: BlaveOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        input_serializer = BlaveOrganizationQuerySerializerV1(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        blaves = list_blaves_service(
            user=request.user,
            organization_id=input_serializer.validated_data["organization_id"],
        )
        serializer = BlaveOutputSerializerV1(blaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Blaves"],
        request=BlaveInputSerializerV1,
        responses={
            201: BlaveOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def post(self, request):
        input_serializer = BlaveInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blave = create_blave_service(
            user=request.user,
            **input_serializer.validated_data,
        )

        output_serializer = BlaveOutputSerializerV1(blave)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BlaveDetailAPIViewV1(BlaveAPIView):
    """Consulta e altera uma blave no contexto da organização selecionada."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Blaves"],
        parameters=[
            OpenApiParameter(
                name="organization_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: BlaveOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def get(self, request, blave_id):
        organization_id = self._get_organization_id(request)
        blave = get_blave_service(
            user=request.user,
            organization_id=organization_id,
            blave_id=blave_id,
        )
        serializer = BlaveOutputSerializerV1(blave)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Blaves"],
        parameters=[
            OpenApiParameter(
                name="organization_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=BlavePartialInputSerializerV1,
        responses={
            200: BlaveOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def patch(self, request, blave_id):
        organization_id = self._get_organization_id(request)
        input_serializer = BlavePartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blave = update_blave_service(
            user=request.user,
            organization_id=organization_id,
            blave_id=blave_id,
            **input_serializer.validated_data,
        )

        output_serializer = BlaveOutputSerializerV1(blave)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Blaves"],
        parameters=[
            OpenApiParameter(
                name="organization_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            204: OpenApiResponse(description="Blave excluída."),
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def delete(self, request, blave_id):
        organization_id = self._get_organization_id(request)
        delete_blave_service(
            user=request.user,
            organization_id=organization_id,
            blave_id=blave_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _get_organization_id(request):
        serializer = BlaveOrganizationQuerySerializerV1(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["organization_id"]
