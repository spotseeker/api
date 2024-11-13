from rest_framework.routers import DefaultRouter

from spotseeker.post.views import PostAPIView

app_name = "post"
router = DefaultRouter()
router.register("", PostAPIView, basename="post")

urlpatterns = [*router.urls]
