from http import HTTPMethod

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from spotseeker.post.models import Post
from spotseeker.post.models import PostBookmark
from spotseeker.post.models import PostComment
from spotseeker.post.models import PostLike

from .serializers import PostCommentSerializer
from .serializers import PostSerializer
from .serializers import PostUpdateSerializer


class PostAPIView(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=[HTTPMethod.POST])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=[HTTPMethod.POST])
    def bookmark(self, request, *args, **kwargs):
        post = self.get_object()
        bookmark, created = PostBookmark.objects.get_or_create(
            post=post, user=request.user
        )
        if not created:
            bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentAPIView(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    lookup_field = "id"

    def list(self, request, post_id):
        queryset = self.queryset.filter(post_id=post_id)
        serializer = PostCommentSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, post_id):
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def update(self, request, post_id):
        instance = self.get_object()
        serializer = PostCommentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def destroy(self, request, post_id):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
