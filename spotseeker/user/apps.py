import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "spotseeker.user"
    verbose_name = _("User")

    def ready(self):
        with contextlib.suppress(ImportError):
            import spotseeker.user.signals  # noqa: F401
