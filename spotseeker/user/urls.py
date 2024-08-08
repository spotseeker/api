from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from spotseeker.user.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("", UserViewSet)

app_name = "user"

urlpatterns = [*router.urls]
