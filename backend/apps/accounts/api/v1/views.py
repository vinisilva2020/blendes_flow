from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.api.v1.serializers import (
    AccountOutputSerializerV1,
    AccountPartialInputSerializerV1,
    AccountRegistrationInputSerializerV1,
)
from apps.accounts.common.throttles import RegistrationRateThrottle
from apps.accounts.common.views import AccountAPIView
from apps.accounts.services import (
    create_account_service,
    delete_current_account_service,
    get_current_account_service,
    update_current_account_service,
)
from apps.authentication.api.v1.serializers import APIErrorSerializerV1


class AccountsAPIViewV1(AccountAPIView):
    """Register a local user account."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [RegistrationRateThrottle]

    @extend_schema(
        tags=["Accounts"],
        request=AccountRegistrationInputSerializerV1,
        responses={
            201: AccountOutputSerializerV1,
            400: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
            429: APIErrorSerializerV1,
        },
        auth=[],
    )
    def post(self, request):
        input_serializer = AccountRegistrationInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = dict(input_serializer.validated_data)
        validated_data.pop("password_confirm")

        account = create_account_service(**validated_data)
        output_serializer = AccountOutputSerializerV1(account)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class CurrentAccountAPIViewV1(AccountAPIView):
    """Retrieve, update or soft-delete the authenticated user's own account."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Accounts"],
        responses={
            200: AccountOutputSerializerV1,
            401: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def get(self, request):
        account = get_current_account_service(request.user)
        serializer = AccountOutputSerializerV1(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Accounts"],
        request=AccountPartialInputSerializerV1,
        responses={
            200: AccountOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def patch(self, request):
        input_serializer = AccountPartialInputSerializerV1(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        account = update_current_account_service(
            request.user,
            **input_serializer.validated_data,
        )
        output_serializer = AccountOutputSerializerV1(account)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Accounts"],
        request=None,
        responses={
            204: OpenApiResponse(description="Account deactivated."),
            401: APIErrorSerializerV1,
        },
    )
    def delete(self, request):
        delete_current_account_service(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
