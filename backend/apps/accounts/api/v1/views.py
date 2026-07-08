from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.api.v1.serializers import (
    AccountGoogleSocialAccountInputSerializerV1,
    AccountOutputSerializerV1,
    AccountPartialInputSerializerV1,
    AccountPasswordInputSerializerV1,
    AccountRegistrationInputSerializerV1,
)
from apps.accounts.common.throttles import RegistrationRateThrottle
from apps.accounts.common.views import AccountAPIView
from apps.accounts.services import (
    create_account_service,
    delete_current_account_service,
    get_current_account_service,
    link_current_google_social_account_service,
    unlink_current_social_account_service,
    update_current_account_service,
    update_current_account_password_service,
)
from apps.authentication.api.v1.serializers import APIErrorSerializerV1
from apps.authentication.models import SocialIdentityProvider


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


class CurrentAccountGoogleSocialAccountAPIViewV1(AccountAPIView):
    """Link or unlink the authenticated user's Google account."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Accounts"],
        request=AccountGoogleSocialAccountInputSerializerV1,
        responses={
            200: AccountOutputSerializerV1,
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            403: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def post(self, request):
        input_serializer = AccountGoogleSocialAccountInputSerializerV1(
            data=request.data,
        )
        input_serializer.is_valid(raise_exception=True)

        link_current_google_social_account_service(
            request.user,
            credential=input_serializer.validated_data["credential"],
        )
        account = get_current_account_service(request.user)
        output_serializer = AccountOutputSerializerV1(account)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Accounts"],
        request=None,
        responses={
            204: OpenApiResponse(description="Google social account unlinked."),
            401: APIErrorSerializerV1,
            404: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def delete(self, request):
        unlink_current_social_account_service(
            request.user,
            provider=SocialIdentityProvider.GOOGLE,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentAccountPasswordAPIViewV1(AccountAPIView):
    """Set or change the authenticated user's local password."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Accounts"],
        request=AccountPasswordInputSerializerV1,
        responses={
            204: OpenApiResponse(description="Local password updated."),
            400: APIErrorSerializerV1,
            401: APIErrorSerializerV1,
            409: APIErrorSerializerV1,
        },
    )
    def put(self, request):
        input_serializer = AccountPasswordInputSerializerV1(
            data=request.data,
            context={"user": request.user},
        )
        input_serializer.is_valid(raise_exception=True)

        update_current_account_password_service(
            request.user,
            current_password=input_serializer.validated_data.get("current_password"),
            new_password=input_serializer.validated_data["new_password"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
