from rest_framework import serializers

from apps.organizations.models import Organization


class OrganizationInputSerializerV1(serializers.Serializer):
    name = serializers.CharField(max_length=255, trim_whitespace=True)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )


class OrganizationPartialInputSerializerV1(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=False,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )


class OrganizationOutputSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
