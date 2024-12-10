from django.urls import path

from spotseeker.location.views import LocationView

app_name = "location"
urlpatterns = [
    path("", LocationView.as_view(), name="location"),
]
