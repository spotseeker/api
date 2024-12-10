from http import HTTPMethod

from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters
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

from spotseeker.post.filters import PostFilter
from spotseeker.post.models import Post
from spotseeker.post.models import PostBookmark
from spotseeker.post.models import PostImage
from spotseeker.post.models import PostLike
from spotseeker.post.serializers import PostSerializer
from spotseeker.post.serializers import PostUpdateSerializer


class PostViewSet(
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PostFilter
    search_fields = ["body", "user__username", "user__first_name", "user__last_name"]
    lookup_field = "id"
    queryset = None

    def get_queryset(self):
        return (
            Post.objects.filter(
                deleted_at=None,
            )
            .annotate(
                likes=Count("postlike", distinct=True),
                comments=Count("postcomment", distinct=True),
                is_liked=Exists(
                    PostLike.objects.filter(
                        post_id=OuterRef("id"), user=self.request.user
                    )
                ),
                is_bookmarked=Exists(
                    PostBookmark.objects.filter(
                        post_id=OuterRef("id"), user=self.request.user
                    )
                ),
            )
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "postimage_set", queryset=PostImage.objects.all(), to_attr="images"
                )
            )
            .order_by("-created_at")
        )

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            id=self.kwargs["id"],
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        filters = [*list(PostFilter.get_filters().keys()), "q"]
        if not any(key in request.query_params for key in filters):
            following = request.user.following.values_list(
                "followed_user_id", flat=True
            )
            queryset = queryset.filter(user_id__in=following, is_archived=False)
        page = self.paginate_queryset(queryset)
        if page is None:
            serializer = self.get_serializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @extend_schema(request=PostUpdateSerializer, responses={200: PostSerializer})
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = self.get_serializer(instance)
        return Response(status=status.HTTP_200_OK, data=response.data)

    @extend_schema(request=PostUpdateSerializer, responses={200: PostSerializer})
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request=None, responses={204: None})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
