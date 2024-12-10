from django.db.models.signals import post_save
from django.dispatch import receiver

from spotseeker.post.models import PostComment
from spotseeker.post.models import PostLike
from spotseeker.user.models import Follow
from spotseeker.user.models import Notification


@receiver(post_save, sender=Follow)
def create_notification_new_follower(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.followed_user,
            user_interaction=instance.follower_user,
            content=f"{instance.follower_user.username} empezó a seguirte",
        )


@receiver(post_save, sender=PostLike)
def create_notification_post_like(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.post.user:
            Notification.objects.create(
                user=instance.post.user,
                user_interaction=instance.user,
                content=f"{instance.user.username} le gustó tu publicación",
            )


@receiver(post_save, sender=PostComment)
def create_notification_new_comment(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.post.user:
            Notification.objects.create(
                user=instance.post.user,
                user_interaction=instance.user,
                content=f"{instance.user.username} comentó tu publicación",
            )
