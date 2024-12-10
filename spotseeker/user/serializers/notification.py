from rest_framework import serializers

from spotseeker.user.models import Notification
from spotseeker.user.serializers.user import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user_interaction = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["user_interaction", "content"]
