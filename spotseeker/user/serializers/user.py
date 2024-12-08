from rest_framework import serializers

from spotseeker.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password",
            "description",
            "avatar",
            "is_validated",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "deleted_at": {"read_only": True},
            "is_validated": {"read_only": True},
        }


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "new_password"]


class RecoverPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]
