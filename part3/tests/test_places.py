import uuid
import pytest
from app import create_app, db
from config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()


@pytest.fixture
def auth_data(client):
    email = f"{uuid.uuid4().hex}@test.com"

    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    assert login_response.status_code == 200

    return {
        "token": login_response.json["access_token"],
        "user_id": response.json["id"]
    }


def create_test_place(client, auth_data):
    response = client.post(
        "/api/v1/places/",
        headers={
            "Authorization": f"Bearer {auth_data['token']}"
        },
        json={
            "title": "Luxury Apartment",
            "description": "Beautiful apartment",
            "price": 350,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": auth_data["user_id"],
            "amenities": []
        }
    )

    assert response.status_code == 201
    return response.json


def test_create_place_success(client, auth_data):
    response = client.post(
        "/api/v1/places/",
        headers={
            "Authorization": f"Bearer {auth_data['token']}"
        },
        json={
            "title": "Beach House",
            "description": "Nice house",
            "price": 500,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": auth_data["user_id"],
            "amenities": []
        }
    )

    assert response.status_code == 201


def test_get_all_places_success(client, auth_data):
    create_test_place(client, auth_data)

    response = client.get("/api/v1/places/")

    assert response.status_code == 200


def test_get_place_by_id_success(client, auth_data):
    place = create_test_place(client, auth_data)

    response = client.get(
        f"/api/v1/places/{place['id']}"
    )

    assert response.status_code == 200


def test_update_place_success(client, auth_data):
    place = create_test_place(client, auth_data)

    response = client.put(
        f"/api/v1/places/{place['id']}",
        headers={
            "Authorization": f"Bearer {auth_data['token']}"
        },
        json={
            "title": "Updated Apartment",
            "price": 450
        }
    )

    assert response.status_code == 200


def test_create_place_invalid_owner(client, auth_data):
    response = client.post(
        "/api/v1/places/",
        headers={
            "Authorization": f"Bearer {auth_data['token']}"
        },
        json={
            "title": "Invalid",
            "description": "test",
            "price": 100,
            "latitude": 24,
            "longitude": 46,
            "owner_id": "wrong",
            "amenities": []
        }
    )

    assert response.status_code == 400


def test_get_place_not_found(client):
    response = client.get(
        "/api/v1/places/not_found"
    )

    assert response.status_code == 404


def test_update_place_not_found(client, auth_data):
    response = client.put(
        "/api/v1/places/not_found",
        headers={
            "Authorization": f"Bearer {auth_data['token']}"
        },
        json={
            "title": "Updated"
        }
    )

    assert response.status_code == 404
