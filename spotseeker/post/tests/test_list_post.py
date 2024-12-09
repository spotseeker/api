import pytest
from django.conf import settings
from rest_framework import status

from spotseeker.post.tests.factories import PostBookmarkFactory
from spotseeker.post.tests.factories import PostFactory
from spotseeker.post.tests.factories import PostImageFactory
from spotseeker.user.tests.factories import FollowFactory
from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_list_posts(api_client, user):
    new_user = UserFactory()
    post = PostFactory(user=user)
    post_images = [PostImageFactory(post=post, order=i + 1) for i in range(3)]
    api_client.force_authenticate(user=new_user)
    FollowFactory(followed_user=user, follower_user=new_user)
    response = api_client.get("/post/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["body"] == post.body
    assert response.data["results"][0]["user"]["username"] == user.username
    assert len(response.data["results"][0]["images"]) == len(post_images)


@pytest.mark.django_db()
def test_list_zero_posts(api_client, user):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.get("/post/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


@pytest.mark.django_db()
def test_list_paginated(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=user, follower_user=new_user)
    posts = PostFactory.create_batch(21, user=user)
    [PostImageFactory(post=post) for post in posts]
    api_client.force_authenticate(user=new_user)
    response = api_client.get("/post/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == len(posts)
    assert len(response.data["results"]) == settings.REST_FRAMEWORK["PAGE_SIZE"]
    assert response.data["next"] is not None
    assert response.data["previous"] is None
    new_response = api_client.get(response.data["next"])
    assert new_response.status_code == status.HTTP_200_OK
    assert len(new_response.data["results"]) == 1
    assert new_response.data["next"] is None
    assert new_response.data["previous"] is not None


@pytest.mark.django_db()
def test_list_posts_not_following(api_client, user):
    new_user = UserFactory()
    PostFactory(user=user)
    api_client.force_authenticate(user=new_user)
    response = api_client.get("/post/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


@pytest.mark.django_db()
def test_list_posts_archived(api_client, user):
    post = PostFactory(user=user, is_archived=True)
    other_post = PostFactory(user=user)
    PostImageFactory(post=post)
    PostImageFactory(post=other_post)
    api_client.force_authenticate(user=user)
    response = api_client.get("/post/?is_archived=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["body"] == post.body
    assert response.data["results"][0]["user"]["username"] == user.username


@pytest.mark.django_db()
def test_list_posts_other_user_archived(api_client, user):
    new_user = UserFactory()
    post = PostFactory(user=user, is_archived=True)
    PostImageFactory(post=post)
    FollowFactory(followed_user=user, follower_user=new_user)
    api_client.force_authenticate(user=new_user)
    response = api_client.get("/post/?is_archived=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


@pytest.mark.django_db()
def test_list_posts_bookmarked(api_client, user):
    post = PostFactory(user=user)
    other_post = PostFactory(user=user)
    PostImageFactory(post=post)
    PostImageFactory(post=other_post)
    PostBookmarkFactory(user=user, post=post)
    api_client.force_authenticate(user=user)
    response = api_client.get("/post/?is_bookmarked=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["body"] == post.body


@pytest.mark.django_db()
def test_list_posts_other_user_bookmarked(api_client, user):
    new_user = UserFactory()
    post = PostFactory(user=new_user)
    PostImageFactory(post=post)
    FollowFactory(followed_user=new_user, follower_user=user)
    PostBookmarkFactory(user=user, post=post)
    api_client.force_authenticate(user=new_user)
    response = api_client.get("/post/?is_bookmarked=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


@pytest.mark.django_db()
def test_list_posts_other_user(api_client, user):
    new_user = UserFactory()
    post = PostFactory(user=new_user)
    other_post = PostFactory(user=new_user, is_archived=True)
    PostImageFactory(post=post)
    PostImageFactory(post=other_post)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/post/?user={new_user.username}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["body"] == post.body
