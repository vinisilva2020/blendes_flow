from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.organizations.api.v1.serializers import (
    OrganizationInputSerializerV1,
    OrganizationOutputSerializerV1,
    OrganizationPartialInputSerializerV1,
)
from apps.organizations.common.views import OrganizationAPIView
from apps.organizations.permissions import IsOrganizationOwner
from apps.organizations.services import (
    create_organization_service,
    delete_organization_service,
    get_user_organization_service,
    list_user_organizations_service,
    update_organization_service,
)


class OrganizationsAPIViewV1(OrganizationAPIView):
    """List and create organizations for the authenticated user."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Organizations"],
        responses={
            200: OrganizationOutputSerializerV1(many=True),
            401: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        organizations = list_user_organizations_service(user=request.user)
        serializer = OrganizationOutputSerializerV1(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Organizations"],
        request=OrganizationInputSerializerV1,
        responses={
            201: OrganizationOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def post(self, request):
        input_serializer = OrganizationInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        organization = create_organization_service(
            user=request.user,
            **input_serializer.validated_data,
        )

        output_serializer = OrganizationOutputSerializerV1(organization)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class OrganizationDetailAPIViewV1(OrganizationAPIView):
    """Retrieve, update and delete one organization for the authenticated user."""

    permission_classes = [
        IsAuthenticated,
        IsOrganizationOwner,
    ]

    @extend_schema(
        tags=["Organizations"],
        responses={
            200: OrganizationOutputSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def get(self, request, organization_id):
        organization = get_user_organization_service(
            user=request.user,
            organization_id=organization_id,
        )
        self.check_object_permissions(request, organization)

        serializer = OrganizationOutputSerializerV1(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Organizations"],
        request=OrganizationPartialInputSerializerV1,
        responses={
            200: OrganizationOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def patch(self, request, organization_id):
        organization = get_user_organization_service(
            user=request.user,
            organization_id=organization_id,
        )
        self.check_object_permissions(request, organization)

        input_serializer = OrganizationPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        organization = update_organization_service(
            user=request.user,
            organization_id=organization_id,
            **input_serializer.validated_data,
        )

        output_serializer = OrganizationOutputSerializerV1(organization)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Organizations"],
        request=None,
        responses={
            204: OpenApiResponse(description="Organization deleted."),
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
        },
    )
    def delete(self, request, organization_id):
        organization = get_user_organization_service(
            user=request.user,
            organization_id=organization_id,
        )
        self.check_object_permissions(request, organization)

        delete_organization_service(
            user=request.user,
            organization_id=organization_id,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
