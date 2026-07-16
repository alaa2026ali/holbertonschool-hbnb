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
    """Create and return a user for place tests."""
    unique_email = f"place_{uuid.uuid4().hex}@example.com"

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


def create_test_place(client):
    """Create and return a place for tests."""
    user = create_test_user(client)

    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Luxury Apartment",
            "description": "Beautiful apartment in Riyadh",
            "price": 350,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user["id"],
            "amenities": []
        }
    )

    assert response.status_code == 201
    return response.json


# ==========================================================
# Success Test Cases
# ==========================================================

def test_create_place_success(client):
    user = create_test_user(client)

    payload = {
        "title": "Beach House",
        "description": "A beautiful house near the beach",
        "price": 500,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "owner_id": user["id"],
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 201
    assert response.json["title"] == "Beach House"
    assert response.json["price"] == 500
    assert response.json["owner"]["id"] == user["id"]
    assert "id" in response.json


def test_get_all_places_success(client):
    create_test_place(client)

    response = client.get("/api/v1/places/")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_place_by_id_success(client):
    place = create_test_place(client)

    response = client.get(f"/api/v1/places/{place['id']}")

    assert response.status_code == 200
    assert response.json["id"] == place["id"]
    assert response.json["title"] == "Luxury Apartment"


def test_update_place_success(client):
    place = create_test_place(client)

    payload = {
        "title": "Updated Apartment",
        "price": 450
    }

    response = client.put(
        f"/api/v1/places/{place['id']}",
        json=payload
    )

    assert response.status_code == 200
    assert response.json["title"] == "Updated Apartment"
    assert response.json["price"] == 450


# ==========================================================
# Validation Test Cases
# ==========================================================

def test_create_place_invalid_owner(client):
    payload = {
        "title": "Invalid Place",
        "description": "Owner does not exist",
        "price": 100,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "owner_id": "non_existing_owner",
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 400


def test_create_place_negative_price(client):
    user = create_test_user(client)

    payload = {
        "title": "Invalid Price Place",
        "description": "Invalid price",
        "price": -50,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "owner_id": user["id"],
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 400


def test_create_place_invalid_latitude(client):
    user = create_test_user(client)

    payload = {
        "title": "Invalid Latitude Place",
        "description": "Invalid latitude",
        "price": 200,
        "latitude": 100,
        "longitude": 46.6753,
        "owner_id": user["id"],
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 400


def test_create_place_invalid_longitude(client):
    user = create_test_user(client)

    payload = {
        "title": "Invalid Longitude Place",
        "description": "Invalid longitude",
        "price": 200,
        "latitude": 24.7136,
        "longitude": 200,
        "owner_id": user["id"],
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 400


def test_create_place_missing_title(client):
    user = create_test_user(client)

    payload = {
        "description": "Missing title",
        "price": 200,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "owner_id": user["id"],
        "amenities": []
    }

    response = client.post("/api/v1/places/", json=payload)

    assert response.status_code == 400


# ==========================================================
# Not Found Test Cases
# ==========================================================

def test_get_place_not_found(client):
    response = client.get("/api/v1/places/non_existing_id")

    assert response.status_code == 404


def test_update_place_not_found(client):
    response = client.put(
        "/api/v1/places/non_existing_id",
        json={"title": "Updated Place"}
    )

    assert response.status_code == 404