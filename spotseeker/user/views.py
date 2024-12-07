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
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from config.serializers import ErrorSerializer
from spotseeker.user.models import Notification
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.utils.email import EmailHelper

from .serializers import EmailSerializer
from .serializers import NotificationSerializer
from .serializers import RecoverPasswordSerializer
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

    @extend_schema(request=RecoverPasswordSerializer)
    @action(detail=False, methods=[HTTPMethod.POST], url_path="password/reset")
    def recover_password(self, request):
        serializer = RecoverPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(serializer.validated_data["password"])
        request.user.password = password
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecoverPasswordView(APIView):
    @extend_schema(request=EmailSerializer, responses={204: None})
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email, deleted_at__isnull=True)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        otp, _ = UserOTP.objects.get_or_create(user=user)
        email = EmailHelper()
        email.send_password_reset_otp(user, otp.otp)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecoverPasswordOTPView(APIView):
    @extend_schema(
        request=UserOTPSerializer,
        responses={200: TokenObtainPairSerializer, 400: ErrorSerializer},
    )
    @transaction.atomic
    def post(self, request):
        serializer = UserOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        try:
            user_otp = UserOTP.objects.get(otp=otp)
        except UserOTP.DoesNotExist:
            data = ErrorSerializer({"error": "Invalid OTP"})
            return Response(data.data, status=status.HTTP_400_BAD_REQUEST)
        user_otp.delete()
        refresh = RefreshToken.for_user(user_otp.user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class NotificationView(GenericViewSet, ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)
