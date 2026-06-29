from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.blendes_flow.common.throttles.facet_description import (
    FacetDescriptionManagementRateThrottle,
)
from apps.blendes_flow.common.views.facet_description import FacetDescriptionAPIView
from apps.blendes_flow.serializers.facet_descriptions import (
    FacetDescriptionInputSerializerV1,
    FacetDescriptionOutputSerializerV1,
    FacetDescriptionPartialInputSerializerV1,
)
from apps.blendes_flow.services.facet_descriptions import (
    create_facet_descriptions_service,
    delete_facet_description_service,
    get_facet_description_service,
    list_facet_descriptions_service,
    update_facet_description_service,
)


class FacetDescriptionsAPIViewV1(FacetDescriptionAPIView):
    """Lista e cadastra facet descriptions dentro de uma schapter."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [FacetDescriptionManagementRateThrottle]

    @extend_schema(
        tags=["FacetDescriptions"],
        responses={
            200: FacetDescriptionOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def get(self, request, schapter_id):
        facet_descriptions = list_facet_descriptions_service(
            user=request.user,
            schapter_id=schapter_id,
        )
        serializer = FacetDescriptionOutputSerializerV1(
            facet_descriptions,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["FacetDescriptions"],
        request=FacetDescriptionInputSerializerV1,
        responses={
            201: FacetDescriptionOutputSerializerV1(many=True),
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def post(self, request, schapter_id):
        input_serializer = FacetDescriptionInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        facet_descriptions = create_facet_descriptions_service(
            user=request.user,
            schapter_id=schapter_id,
            **input_serializer.validated_data,
        )

        output_serializer = FacetDescriptionOutputSerializerV1(
            facet_descriptions,
            many=True,
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class FacetDescriptionDetailAPIViewV1(FacetDescriptionAPIView):
    """Recupera, atualiza e remove uma facet description do usuario."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [FacetDescriptionManagementRateThrottle]

    @extend_schema(
        tags=["FacetDescriptions"],
        responses={
            200: FacetDescriptionOutputSerializerV1,
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
        facet_description = get_facet_description_service(
            user=request.user,
            facet_description_id=facet_description_id,
        )
        serializer = FacetDescriptionOutputSerializerV1(facet_description)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["FacetDescriptions"],
        request=FacetDescriptionPartialInputSerializerV1,
        responses={
            200: FacetDescriptionOutputSerializerV1,
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
        facet_description_id,
    ):
        input_serializer = FacetDescriptionPartialInputSerializerV1(
            data=request.data,
        )
        input_serializer.is_valid(raise_exception=True)

        facet_description = update_facet_description_service(
            user=request.user,
            facet_description_id=facet_description_id,
            **input_serializer.validated_data,
        )
        serializer = FacetDescriptionOutputSerializerV1(facet_description)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["FacetDescriptions"],
        request=None,
        responses={
            204: OpenApiResponse(description="Facet description deleted."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
    )
    def delete(
        self,
        request,
        facet_description_id,
    ):
        delete_facet_description_service(
            user=request.user,
            facet_description_id=facet_description_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
