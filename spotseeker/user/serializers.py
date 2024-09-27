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
            "url",
            "password",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "password": {"write_only": True},
        }


def create(self, validated_data):
    user = User(
        username=validated_data["username"],
        email=validated_data["email"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        birth_date=validated_data["birth_date"],
    )
    user.set_password(validated_data["password"])  # Encriptar la contraseña
    user.save()
    return user
