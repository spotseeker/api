from django.urls import path
from rest_framework.routers import DefaultRouter

from spotseeker.post.views import PostAPIView
from spotseeker.post.views import PostCommentAPIView

app_name = "post"
post_router = DefaultRouter()
post_router.register("", PostAPIView, basename="post")


urlpatterns = [
    *post_router.urls,
    path(
        "<uuid:post_id>/comment/",
        PostCommentAPIView.as_view({"get": "list", "post": "create"}),
        name="comment",
    ),
    path(
        "<uuid:post_id>/comment/<uuid:pk>/",
        PostCommentAPIView.as_view({"put": "update", "delete": "destroy"}),
        name="comment-detail",
    ),
]
