from rest_framework import serializers

from spotseeker.user.models import UserOTP


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ["otp"]
