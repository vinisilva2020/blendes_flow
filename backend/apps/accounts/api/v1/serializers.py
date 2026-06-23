from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


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


class AccountOutputSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "avatar_type",
            "is_active",
            "date_joined",
        ]
        read_only_fields = fields
