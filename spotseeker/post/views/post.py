from http import HTTPMethod

from django.db.models import Count
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from spotseeker.post.models import Post
from spotseeker.post.models import PostBookmark
from spotseeker.post.models import PostComment
from spotseeker.post.models import PostImage
from spotseeker.post.models import PostLike
from spotseeker.post.serializers import PostSerializer
from spotseeker.post.serializers import PostUpdateSerializer


class PostAPIView(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        following = request.user.following.values_list("followed_user_id", flat=True)
        queryset = (
            self.queryset.filter(
                deleted_at=None, is_archived=False, user_id__in=following
            )
            .annotate(
                likes=Subquery(
                    PostLike.objects.filter(post_id=OuterRef("id"))
                    .values("id")
                    .annotate(count=Count("id"))
                    .values("count")
                ),
                comments=Subquery(
                    PostComment.objects.filter(post_id=OuterRef("id"))
                    .values("id")
                    .annotate(count=Count("id"))
                    .values("count")
                ),
            )
            .prefetch_related(
                Prefetch(
                    "postimage_set", queryset=PostImage.objects.all(), to_attr="images"
                )
            )
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @extend_schema(request=PostUpdateSerializer, responses={200: PostUpdateSerializer})
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(request=None, responses={204: None})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None, responses={204: None})
    @action(detail=True, methods=[HTTPMethod.POST])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None, responses={204: None})
    @action(detail=True, methods=[HTTPMethod.POST])
    def bookmark(self, request, *args, **kwargs):
        post = self.get_object()
        bookmark, created = PostBookmark.objects.get_or_create(
            post=post, user=request.user
        )
        if not created:
            bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
