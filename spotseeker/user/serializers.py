from rest_framework import serializers

from spotseeker.user.models import Notification
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ["otp"]


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "new_password", "confirm_password"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user", "user_interaction", "content"]
