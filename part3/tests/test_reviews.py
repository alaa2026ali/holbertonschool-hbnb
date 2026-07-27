import uuid
import pytest
from run import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    email = f"{uuid.uuid4().hex}@test.com"

    client.post(
        "/api/v1/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    return response.json["access_token"]


def create_test_user(client):
    email = f"{uuid.uuid4().hex}@example.com"

    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Noura",
            "last_name": "Fahad",
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 201
    return response.json


def create_test_place(client, auth_token):
    user = create_test_user(client)

    response = client.post(
        "/api/v1/places/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Review Apartment",
            "description": "Place for review",
            "price": 300,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user["id"],
            "amenities": []
        }
    )

    assert response.status_code == 201
    return response.json, user


def create_test_review(client, auth_token):

    place, user = create_test_place(client, auth_token)

    response = client.post(
        "/api/v1/reviews/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Great apartment",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        }
    )

    assert response.status_code == 201
    return response.json


def test_create_review_success(client, auth_token):

    review = create_test_review(client, auth_token)

    assert review["rating"] == 5
    assert review["text"] == "Great apartment"


def test_get_all_reviews_success(client, auth_token):

    create_test_review(client, auth_token)

    response = client.get(
        "/api/v1/reviews/"
    )

    assert response.status_code == 200


def test_get_review_by_id_success(client, auth_token):

    review = create_test_review(client, auth_token)

    response = client.get(
        f"/api/v1/reviews/{review['id']}"
    )

    assert response.status_code == 200


def test_update_review_success(client, auth_token):

    review = create_test_review(client, auth_token)

    response = client.put(
        f"/api/v1/reviews/{review['id']}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Updated review",
            "rating": 4
        }
    )

    assert response.status_code == 200


def test_delete_review_success(client, auth_token):

    review = create_test_review(client, auth_token)

    response = client.delete(
        f"/api/v1/reviews/{review['id']}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 204


def test_get_reviews_by_place_success(client, auth_token):

    place, user = create_test_place(client, auth_token)

    client.post(
        "/api/v1/reviews/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Nice",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        }
    )

    response = client.get(
        f"/api/v1/places/{place['id']}/reviews"
    )

    assert response.status_code == 200


def test_create_review_invalid_user(client, auth_token):

    place, _ = create_test_place(client, auth_token)

    response = client.post(
        "/api/v1/reviews/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Bad user",
            "rating": 5,
            "user_id": "wrong_id",
            "place_id": place["id"]
        }
    )

    assert response.status_code == 400


def test_create_review_invalid_place(client, auth_token):

    user = create_test_user(client)

    response = client.post(
        "/api/v1/reviews/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Bad place",
            "rating": 5,
            "user_id": user["id"],
            "place_id": "wrong_id"
        }
    )

    assert response.status_code == 400


def test_update_review_not_found(client, auth_token):

    response = client.put(
        "/api/v1/reviews/non_existing_id",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "text": "Updated",
            "rating": 4
        }
    )

    assert response.status_code == 404


def test_delete_review_not_found(client, auth_token):

    response = client.delete(
        "/api/v1/reviews/non_existing_id",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 404
