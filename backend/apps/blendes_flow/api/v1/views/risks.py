from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.risk import RiskManagementRateThrottle
from apps.blendes_flow.common.views.risk import RiskAPIView
from apps.blendes_flow.serializers.risks import (
    RiskInputSerializerV1,
    RiskOutputSerializerV1,
    RiskPartialInputSerializerV1,
)
from apps.blendes_flow.services.risks import (
    create_risks_service,
    delete_risk_service,
    get_risk_service,
    list_risks_service,
    update_risk_service,
)


class RisksAPIViewV1(RiskAPIView):
    """Lista e cadastra riscos dentro de uma facet description."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [RiskManagementRateThrottle]

    @extend_schema(
        tags=["Risks"],
        responses={
            200: RiskOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(
        self,
        request,
        facet_description_id,
    ):
        risks = list_risks_service(
            user=request.user,
            facet_description_id=facet_description_id,
        )
        serializer = RiskOutputSerializerV1(risks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Risks"],
        request=RiskInputSerializerV1,
        responses={
            201: RiskOutputSerializerV1(many=True),
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
        facet_description_id,
    ):
        input_serializer = RiskInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        risks = create_risks_service(
            user=request.user,
            facet_description_id=facet_description_id,
            **input_serializer.validated_data,
        )

        output_serializer = RiskOutputSerializerV1(risks, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class RiskDetailAPIViewV1(RiskAPIView):
    """Recupera, atualiza e remove um risco do usuario."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [RiskManagementRateThrottle]

    @extend_schema(
        tags=["Risks"],
        responses={
            200: RiskOutputSerializerV1,
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
        risk = get_risk_service(
            user=request.user,
            risk_id=risk_id,
        )
        serializer = RiskOutputSerializerV1(risk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Risks"],
        request=RiskPartialInputSerializerV1,
        responses={
            200: RiskOutputSerializerV1,
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
        risk_id,
    ):
        input_serializer = RiskPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        risk = update_risk_service(
            user=request.user,
            risk_id=risk_id,
            **input_serializer.validated_data,
        )
        serializer = RiskOutputSerializerV1(risk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Risks"],
        request=None,
        responses={
            204: OpenApiResponse(description="Risk deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(
        self,
        request,
        risk_id,
    ):
        delete_risk_service(
            user=request.user,
            risk_id=risk_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
