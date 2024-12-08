from django.urls import path
from rest_framework.routers import DefaultRouter

from spotseeker.post.views import PostCommentView
from spotseeker.post.views import PostViewSet

app_name = "post"
post_router = DefaultRouter()
post_router.register("", PostViewSet, basename="post")


urlpatterns = [
    *post_router.urls,
    path(
        "<uuid:post_id>/comment/",
        PostCommentView.as_view({"get": "list", "post": "create"}),
        name="comment",
    ),
    path(
        "<uuid:post_id>/comment/<uuid:pk>/",
        PostCommentView.as_view({"put": "update", "delete": "destroy"}),
        name="comment-detail",
    ),
]
