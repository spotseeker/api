from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from config.models import BaseTimestampedModel


class User(AbstractUser, BaseModel, BaseTimestampedModel):
    """
    Default custom user model for spotseeker.
    """

    is_active = None
    email = models.EmailField(_("email address"), unique=True)
    birth_date = models.DateField(_("birth date"))
    description = models.TextField(_("profile bio"), blank=True)
    avatar = models.URLField(_("URL of the profile picture"), blank=True)
    is_validated = models.BooleanField(_("if the email is validated"), default=False)


class UserOTP(models.Model):
    otp = models.CharField(_("code for validations"), max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Register created timestamp",
    )

    def __str__(self):
        return self.otp


class Follow(models.Model):
    following_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Register created timestamp",
    )

    def __str__(self):
        return f"{self.following_user.username} follows {self.followed_user.username}"


class Notification(BaseTimestampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    user_interaction = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_interaction"
    )
    content = models.TextField(_("Content of the notification"))

    def __str__(self):
        return self.message
