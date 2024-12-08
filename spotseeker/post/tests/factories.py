from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from spotseeker.post.models import Post
from spotseeker.post.models import PostBookmark
from spotseeker.post.models import PostComment
from spotseeker.post.models import PostImage
from spotseeker.user.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    body = Faker("text")
    location_id = Faker("uuid4")
    score = Faker("random_int", min=1, max=5)

    class Meta:
        model = Post


class PostImageFactory(DjangoModelFactory):
    media = Faker("url")
    order = Faker("random_int", min=1, max=3)
    post = SubFactory(PostFactory)

    class Meta:
        model = PostImage


class PostBookmarkFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    user = SubFactory("spotseeker.user.tests.factories.UserFactory")

    class Meta:
        model = PostBookmark


class PostCommentFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    user = SubFactory(UserFactory)
    comment = Faker("text")

    class Meta:
        model = PostComment
