from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.mixpoint import (
    MixpointManagementRateThrottle,
)
from apps.blendes_flow.common.views.mixpoint import MixpointAPIView
from apps.blendes_flow.serializers.mixpoints import (
    MixpointInputSerializerV1,
    MixpointOutputSerializerV1,
    MixpointPartialInputSerializerV1,
)
from apps.blendes_flow.services.mixpoints import (
    create_mixpoints_service,
    delete_mixpoint_service,
    get_mixpoint_service,
    list_mixpoints_service,
    update_mixpoint_service,
)


class MixpointsAPIViewV1(MixpointAPIView):
    """Lista e cadastra mixpoints dentro de uma acao concreta."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [MixpointManagementRateThrottle]

    @extend_schema(
        tags=["Mixpoints"],
        responses={
            200: MixpointOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(
        self,
        request,
        concrete_action_id,
    ):
        mixpoints = list_mixpoints_service(
            user=request.user,
            concrete_action_id=concrete_action_id,
        )
        serializer = MixpointOutputSerializerV1(mixpoints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Mixpoints"],
        request=MixpointInputSerializerV1,
        responses={
            201: MixpointOutputSerializerV1(many=True),
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
        concrete_action_id,
    ):
        input_serializer = MixpointInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        mixpoints = create_mixpoints_service(
            user=request.user,
            concrete_action_id=concrete_action_id,
            **input_serializer.validated_data,
        )

        output_serializer = MixpointOutputSerializerV1(mixpoints, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class MixpointDetailAPIViewV1(MixpointAPIView):
    """Recupera, atualiza e remove um mixpoint do usuario."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [MixpointManagementRateThrottle]

    @extend_schema(
        tags=["Mixpoints"],
        responses={
            200: MixpointOutputSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(
        self,
        request,
        mixpoint_id,
    ):
        mixpoint = get_mixpoint_service(
            user=request.user,
            mixpoint_id=mixpoint_id,
        )
        serializer = MixpointOutputSerializerV1(mixpoint)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Mixpoints"],
        request=MixpointPartialInputSerializerV1,
        responses={
            200: MixpointOutputSerializerV1,
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
        mixpoint_id,
    ):
        input_serializer = MixpointPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        mixpoint = update_mixpoint_service(
            user=request.user,
            mixpoint_id=mixpoint_id,
            **input_serializer.validated_data,
        )
        serializer = MixpointOutputSerializerV1(mixpoint)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Mixpoints"],
        request=None,
        responses={
            204: OpenApiResponse(description="Mixpoint deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(
        self,
        request,
        mixpoint_id,
    ):
        delete_mixpoint_service(
            user=request.user,
            mixpoint_id=mixpoint_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
