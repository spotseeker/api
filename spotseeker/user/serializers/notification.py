from rest_framework import serializers

from spotseeker.user.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user", "user_interaction", "content"]
