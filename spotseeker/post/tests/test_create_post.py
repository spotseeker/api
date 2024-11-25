import pytest
from rest_framework import status

from spotseeker.post.tests.factories import PostFactory
from spotseeker.post.tests.factories import PostImageFactory


@pytest.mark.django_db()
def test_create_post(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    image = PostImageFactory.build(post=post, order=1)
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "location_id": post.location_id,
            "images": [{"media": image.media, "order": 1}],
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["body"] == post.body
    assert response.data["score"] == post.score
    assert len(response.data["images"]) == 1


@pytest.mark.django_db()
def test_create_post_multiple_images(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    images = PostImageFactory.build_batch(3, post=post)
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "location_id": post.location_id,
            "images": [
                {"media": image.media, "order": i + 1} for i, image in enumerate(images)
            ],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["body"] == post.body
    assert response.data["score"] == post.score
    assert len(response.data["images"]) == len(images)


@pytest.mark.django_db()
def test_fail_exceeded_number_of_images(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    images = PostImageFactory.build_batch(4, post=post)
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "location_id": post.location_id,
            "images": [
                {"media": image.media, "order": image.order} for image in images
            ],
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["images"][0] == "You can only upload up to 3 images."


@pytest.mark.django_db()
def test_fail_empty_location(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    image = PostImageFactory.build(post=post)
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "images": [{"media": image.media, "order": image.order}],
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["location_id"][0] == "This field is required."


@pytest.mark.django_db()
def test_fail_empty_images(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "location_id": post.location_id,
            "images": [],
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["images"][0] == "You must upload at least one image."


@pytest.mark.django_db()
def test_fail_images_order_repeated(api_client, user):
    api_client.force_authenticate(user=user)
    post = PostFactory.build()
    images = PostImageFactory.build_batch(2, post=post)
    response = api_client.post(
        "/post/",
        {
            "body": post.body,
            "score": post.score,
            "location_id": post.location_id,
            "images": [{"media": image.media, "order": 1} for image in images],
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["images"][0] == "Order of images must be unique."
