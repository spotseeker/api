from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "spotseeker.post"
    verbose_name = _("Post")
