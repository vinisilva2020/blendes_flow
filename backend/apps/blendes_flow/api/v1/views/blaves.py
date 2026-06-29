from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.blave import BlaveManagementRateThrottle
from apps.blendes_flow.common.views.blave import BlaveAPIView
from apps.blendes_flow.serializers.blaves import (
    BlaveInputSerializerV1,
    BlaveOutputSerializerV1,
    BlavePartialInputSerializerV1,
)
from apps.blendes_flow.services.blaves import (
    create_blave_service,
    delete_blave_service,
    get_blave_service,
    list_blaves_service,
    update_blave_service,
)


class BlavesAPIViewV1(BlaveAPIView):
    """Lista e cadastra blaves dentro de uma organizacao."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [BlaveManagementRateThrottle]

    @extend_schema(
        tags=["Blaves"],
        responses={
            200: BlaveOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, organization_id):
        blaves = list_blaves_service(
            user=request.user,
            organization_id=organization_id,
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
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def post(self, request, organization_id):
        input_serializer = BlaveInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blave = create_blave_service(
            user=request.user,
            organization_id=organization_id,
            **input_serializer.validated_data,
        )

        output_serializer = BlaveOutputSerializerV1(blave)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BlaveDetailAPIViewV1(BlaveAPIView):
    """Recupera, atualiza e remove uma blave do usuario autenticado."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [BlaveManagementRateThrottle]

    @extend_schema(
        tags=["Blaves"],
        responses={
            200: BlaveOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, blave_id):
        blave = get_blave_service(
            user=request.user,
            blave_id=blave_id,
        )
        serializer = BlaveOutputSerializerV1(blave)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Blaves"],
        request=BlavePartialInputSerializerV1,
        responses={
            200: BlaveOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def patch(self, request, blave_id):
        input_serializer = BlavePartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blave = update_blave_service(
            user=request.user,
            blave_id=blave_id,
            **input_serializer.validated_data,
        )
        serializer = BlaveOutputSerializerV1(blave)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Blaves"],
        request=None,
        responses={
            204: OpenApiResponse(description="Blave deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(self, request, blave_id):
        delete_blave_service(
            user=request.user,
            blave_id=blave_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
