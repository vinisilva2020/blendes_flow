from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.authentication.models import SocialIdentity


class AccountRegistrationInputSerializerV1(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        trim_whitespace=True,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        style={"input_type": "password"},
    )
    avatar_type = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )

        return data


class AccountPartialInputSerializerV1(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=False,
        trim_whitespace=True,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=254, required=False)
    avatar_type = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )

    def validate_email(self, value):
        return value.strip().lower()


class AccountPasswordInputSerializerV1(serializers.Serializer):
    current_password = serializers.CharField(
        max_length=128,
        required=False,
        trim_whitespace=False,
        write_only=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, data):
        user = self.context.get("user")
        if data["new_password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )

        if user is not None and user.has_usable_password():
            current_password = data.get("current_password")
            if not current_password:
                raise serializers.ValidationError(
                    {"current_password": "Current password is required."}
                )

        return data


class AccountGoogleSocialAccountInputSerializerV1(serializers.Serializer):
    credential = serializers.CharField(
        trim_whitespace=False,
        write_only=True,
    )


class SocialAccountOutputSerializerV1(serializers.ModelSerializer):
    can_unlink = serializers.SerializerMethodField()

    class Meta:
        model = SocialIdentity
        fields = [
            "provider",
            "email",
            "email_verified",
            "can_unlink",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.BooleanField)
    def get_can_unlink(self, obj):
        can_unlink = self.context.get("can_unlink_social_accounts")
        if can_unlink is not None:
            return can_unlink

        return obj.user.has_usable_password() or obj.user.social_identities.count() > 1


class AccountOutputSerializerV1(serializers.ModelSerializer):
    social_accounts = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "avatar_type",
            "social_accounts",
            "is_active",
            "date_joined",
        ]
        read_only_fields = fields

    @extend_schema_field(SocialAccountOutputSerializerV1(many=True))
    def get_social_accounts(self, obj):
        identities = getattr(obj, "prefetched_social_identities", None)
        if identities is None:
            identities = obj.social_identities.only(
                "provider",
                "email",
                "email_verified",
                "created_at",
                "updated_at",
            ).order_by("provider")

        identity_count = len(identities) if isinstance(identities, list) else identities.count()
        can_unlink = obj.has_usable_password() or identity_count > 1
        return SocialAccountOutputSerializerV1(
            identities,
            many=True,
            context={"can_unlink_social_accounts": can_unlink},
        ).data
