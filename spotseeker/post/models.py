from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from config.models import BaseTimestampedModel
from spotseeker.user.models import User


class Post(BaseModel, BaseTimestampedModel):
    body = models.TextField(_("description of the post"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_id = models.TextField(_("google maps location id"))
    score = models.IntegerField(_("score of the location"), null=True, blank=True)
    is_archived = models.BooleanField(_("if the post is not public"), default=False)

    def __str__(self):
        return self.id


class PostImage(BaseTimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media = models.URLField(_("URL of the image"))
    order = models.IntegerField(_("number of the position"))

    def __str__(self):
        return f"Image {self.order} of post {self.post}"


class PostComment(BaseModel, BaseTimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(_("comment in the post"))

    def __str__(self):
        return self.comment


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"user {self.user} liked post {self.post}"


class PostBookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"user {self.user} bookmarked post {self.post}"
