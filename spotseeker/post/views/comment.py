from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from spotseeker.post.models import PostComment
from spotseeker.post.serializers import PostCommentSerializer


class PostCommentAPIView(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    lookup_field = "post_id"

    def list(self, request, post_id):
        queryset = self.queryset.filter(post_id=post_id)
        serializer = PostCommentSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, post_id):
        serializer = PostCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def update(self, request, post_id, pk):
        instance = self.get_object()
        serializer = PostCommentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(request=None, responses={204: None})
    def destroy(self, request, post_id, pk):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
