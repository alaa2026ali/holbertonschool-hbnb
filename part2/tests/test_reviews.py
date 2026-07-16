import uuid

import pytest
from run import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def create_test_user(client):
    """Create and return a user for review tests."""
    unique_email = f"review_{uuid.uuid4().hex}@example.com"

    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Noura",
            "last_name": "Fahad",
            "email": unique_email
        }
    )

    assert response.status_code == 201
    return response.json


def create_test_place(client, user_id):
    """Create and return a place for review tests."""
    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Review Test Apartment",
            "description": "Place used for review tests",
            "price": 300,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id,
            "amenities": []
        }
    )

    assert response.status_code == 201
    return response.json


def create_test_review(client):
    """Create and return a user, place, and review."""
    user = create_test_user(client)
    place = create_test_place(client, user["id"])

    response = client.post(
        "/api/v1/reviews/",
        json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        }
    )

    assert response.status_code == 201
    return user, place, response.json


# ==========================================================
# Success Test Cases
# ==========================================================

def test_create_review_success(client):
    user = create_test_user(client)
    place = create_test_place(client, user["id"])

    payload = {
        "text": "Excellent place and location",
        "rating": 5,
        "user_id": user["id"],
        "place_id": place["id"]
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 201
    assert response.json["text"] == "Excellent place and location"
    assert response.json["rating"] == 5
    assert response.json["user"]["id"] == user["id"]
    assert response.json["place"]["id"] == place["id"]
    assert "id" in response.json


def test_get_all_reviews_success(client):
    create_test_review(client)

    response = client.get("/api/v1/reviews/")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_review_by_id_success(client):
    _, _, review = create_test_review(client)

    response = client.get(f"/api/v1/reviews/{review['id']}")

    assert response.status_code == 200
    assert response.json["id"] == review["id"]
    assert response.json["text"] == "Amazing place!"


def test_update_review_success(client):
    _, _, review = create_test_review(client)

    payload = {
        "text": "Updated review text",
        "rating": 4
    }

    response = client.put(
        f"/api/v1/reviews/{review['id']}",
        json=payload
    )

    assert response.status_code == 200
    assert response.json["text"] == "Updated review text"
    assert response.json["rating"] == 4


def test_delete_review_success(client):
    _, _, review = create_test_review(client)

    response = client.delete(f"/api/v1/reviews/{review['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/reviews/{review['id']}")
    assert get_response.status_code == 404


def test_get_reviews_by_place_success(client):
    _, place, review = create_test_review(client)

    response = client.get(
        f"/api/v1/places/{place['id']}/reviews"
    )

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) >= 1
    assert response.json[0]["id"] == review["id"]
    assert response.json[0]["place_id"] == place["id"]


# ==========================================================
# Validation Test Cases
# ==========================================================

def test_create_review_empty_text(client):
    user = create_test_user(client)
    place = create_test_place(client, user["id"])

    payload = {
        "text": "",
        "rating": 5,
        "user_id": user["id"],
        "place_id": place["id"]
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 400


def test_create_review_invalid_rating(client):
    user = create_test_user(client)
    place = create_test_place(client, user["id"])

    payload = {
        "text": "Invalid rating",
        "rating": 6,
        "user_id": user["id"],
        "place_id": place["id"]
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 400


def test_create_review_invalid_user(client):
    user = create_test_user(client)
    place = create_test_place(client, user["id"])

    payload = {
        "text": "Invalid user",
        "rating": 4,
        "user_id": "non_existing_user",
        "place_id": place["id"]
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 400


def test_create_review_invalid_place(client):
    user = create_test_user(client)

    payload = {
        "text": "Invalid place",
        "rating": 4,
        "user_id": user["id"],
        "place_id": "non_existing_place"
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 400


def test_update_review_invalid_rating(client):
    _, _, review = create_test_review(client)

    response = client.put(
        f"/api/v1/reviews/{review['id']}",
        json={"rating": 10}
    )

    assert response.status_code == 400


# ==========================================================
# Not Found Test Cases
# ==========================================================

def test_get_review_not_found(client):
    response = client.get("/api/v1/reviews/non_existing_id")

    assert response.status_code == 404


def test_update_review_not_found(client):
    response = client.put(
        "/api/v1/reviews/non_existing_id",
        json={
            "text": "Updated review",
            "rating": 4
        }
    )

    assert response.status_code == 404


def test_delete_review_not_found(client):
    response = client.delete("/api/v1/reviews/non_existing_id")

    assert response.status_code == 404


def test_get_reviews_for_missing_place(client):
    response = client.get(
        "/api/v1/places/non_existing_place/reviews"
    )

    assert response.status_code == 404