from django.contrib.auth.hashers import make_password
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.user.serializers import UserSerializer
from spotseeker.user.serializers.user import UserAvailableSearchSerializer
from spotseeker.user.serializers.user import UserAvailableSerializer
from spotseeker.utils.email import EmailHelper


class UserCreateView(CreateAPIView, ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = None

    @transaction.atomic
    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        password = make_password(password)
        user = serializer.save(password=password)
        otp = UserOTP.objects.create(user=user)
        email = EmailHelper()
        email.send_onboarding_otp(user, otp.otp)

    @extend_schema(
        description="Check if a username or email is used",
        parameters=[UserAvailableSearchSerializer],
        responses={200: UserAvailableSerializer},
    )
    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        email = request.query_params.get("email")
        if username is None and email is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        exists_username = (
            self.queryset.filter(username=username).exists() if username else False
        )
        exists_email = self.queryset.filter(email=email).exists() if email else False
        serializer = UserAvailableSerializer(
            {"username": exists_username, "email": exists_email}
        )
        return Response(serializer.data)
