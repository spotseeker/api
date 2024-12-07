from rest_framework import serializers

from spotseeker.user.models import Notification
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(source="followers.count()", read_only=True)
    following = serializers.IntegerField(source="following.count()", read_only=True)

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
            "followers",
            "following",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "deleted_at": {"read_only": True},
            "is_validated": {"read_only": True},
        }


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ["otp"]


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "new_password"]


class RecoverPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user", "user_interaction", "content"]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
