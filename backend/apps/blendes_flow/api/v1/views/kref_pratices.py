from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.kref_pratice import (
    KrefPraticeManagementRateThrottle,
)
from apps.blendes_flow.common.views.kref_pratice import KrefPraticeAPIView
from apps.blendes_flow.serializers.kref_pratices import (
    KrefPraticeInputSerializerV1,
    KrefPraticeOutputSerializerV1,
    KrefPraticePartialInputSerializerV1,
)
from apps.blendes_flow.services.kref_pratices import (
    create_kref_pratices_service,
    delete_kref_pratice_service,
    get_kref_pratice_service,
    list_kref_pratices_service,
    update_kref_pratice_service,
)


class KrefPraticesAPIViewV1(KrefPraticeAPIView):
    """Lista e cadastra praticas KREF dentro de um risco."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [KrefPraticeManagementRateThrottle]

    @extend_schema(
        tags=["KREF Practices"],
        responses={
            200: KrefPraticeOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(
        self,
        request,
        risk_id,
    ):
        kref_pratices = list_kref_pratices_service(
            user=request.user,
            risk_id=risk_id,
        )
        serializer = KrefPraticeOutputSerializerV1(kref_pratices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["KREF Practices"],
        request=KrefPraticeInputSerializerV1,
        responses={
            201: KrefPraticeOutputSerializerV1(many=True),
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def post(
        self,
        request,
        risk_id,
    ):
        input_serializer = KrefPraticeInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        kref_pratices = create_kref_pratices_service(
            user=request.user,
            risk_id=risk_id,
            **input_serializer.validated_data,
        )

        output_serializer = KrefPraticeOutputSerializerV1(kref_pratices, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class KrefPraticeDetailAPIViewV1(KrefPraticeAPIView):
    """Recupera, atualiza e remove uma pratica KREF do usuario."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [KrefPraticeManagementRateThrottle]

    @extend_schema(
        tags=["KREF Practices"],
        responses={
            200: KrefPraticeOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(
        self,
        request,
        kref_pratice_id,
    ):
        kref_pratice = get_kref_pratice_service(
            user=request.user,
            kref_pratice_id=kref_pratice_id,
        )
        serializer = KrefPraticeOutputSerializerV1(kref_pratice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["KREF Practices"],
        request=KrefPraticePartialInputSerializerV1,
        responses={
            200: KrefPraticeOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def patch(
        self,
        request,
        kref_pratice_id,
    ):
        input_serializer = KrefPraticePartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        kref_pratice = update_kref_pratice_service(
            user=request.user,
            kref_pratice_id=kref_pratice_id,
            **input_serializer.validated_data,
        )
        serializer = KrefPraticeOutputSerializerV1(kref_pratice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["KREF Practices"],
        request=None,
        responses={
            204: OpenApiResponse(description="KREF practice deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(
        self,
        request,
        kref_pratice_id,
    ):
        delete_kref_pratice_service(
            user=request.user,
            kref_pratice_id=kref_pratice_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
