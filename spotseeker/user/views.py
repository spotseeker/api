from http import HTTPMethod

from django.contrib.auth.hashers import make_password
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.serializers import ErrorSerializer
from spotseeker.user.models import Notification
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.utils.email import EmailHelper

from .serializers import NotificationSerializer
from .serializers import UserOTPSerializer
from .serializers import UserPasswordUpdateSerializer
from .serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        password = make_password(password)
        user = serializer.save(password=password)
        otp = UserOTP.objects.create(user=user)
        email = EmailHelper()
        email.send_onboarding_otp(user, otp.otp)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @extend_schema(
        request=UserOTPSerializer, responses={204: None, 400: ErrorSerializer}
    )
    @action(detail=False, methods=[HTTPMethod.POST])
    def otp(self, request):
        serializer = UserOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        try:
            user_otp = UserOTP.objects.get(otp=otp, user=request.user)
        except UserOTP.DoesNotExist:
            data = ErrorSerializer({"error": "Invalid OTP"})
            return Response(data.data, status=status.HTTP_400_BAD_REQUEST)
        user_otp.delete()
        request.user.is_validated = True
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=UserPasswordUpdateSerializer)
    @action(detail=False, methods=[HTTPMethod.PATCH])
    def password(self, request):
        serializer = UserPasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationView(GenericViewSet, ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)
