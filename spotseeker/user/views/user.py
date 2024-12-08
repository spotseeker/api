from http import HTTPMethod

from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.serializers import ErrorSerializer
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.user.serializers import RecoverPasswordSerializer
from spotseeker.user.serializers import UserOTPSerializer
from spotseeker.user.serializers import UserPasswordUpdateSerializer
from spotseeker.user.serializers import UserSerializer


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
