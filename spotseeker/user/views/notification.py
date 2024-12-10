from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from spotseeker.user.models import Notification
from spotseeker.user.serializers import NotificationSerializer


class NotificationView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.filter(deleted_at=None).select_related(
        "user_interaction"
    )

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)
