import pytest

from app import create_app, db
from config import TestingConfig


@pytest.fixture
def client():
    """Create Flask test client."""
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()


# ==========================================================
# Success Test Cases
# ==========================================================

def test_create_user_success(client):
    payload = {
        "first_name": "Fahad",
        "last_name": "Alotaibi",
        "email": "fahad_test@example.com",
        "password": "123456"
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201
    assert response.json["first_name"] == "Fahad"
    assert response.json["last_name"] == "Alotaibi"
    assert response.json["email"] == "fahad_test@example.com"
    assert "id" in response.json


def test_get_all_users(client):
    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    assert isinstance(response.json, list)


# ==========================================================
# Validation Test Cases
# ==========================================================

def test_create_user_invalid_email(client):
    payload = {
        "first_name": "Ali",
        "last_name": "Test",
        "email": "abc",
        "password": "123456"

    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_empty_first_name(client):
    payload = {
        "first_name": "",
        "last_name": "Test",
        "email": "test@example.com",
        "password": "123456"

    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_long_first_name(client):
    payload = {
        "first_name": "A" * 51,
        "last_name": "Test",
        "email": "long@example.com",
        "password": "123456"
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_missing_last_name(client):
    payload = {
        "first_name": "Ali",
        "email": "ali@example.com",
        "password": "123456"

    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


# ==========================================================
# Not Found Test Cases
# ==========================================================

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/non_existing_id")

    assert response.status_code == 404


def test_update_user_not_found(client):
    payload = {
        "first_name": "Ali",
        "last_name": "Alharbi",
        "email": "ali@example.com"
    }

    response = client.put(
        "/api/v1/users/non_existing_id",
        json=payload
    )

    assert response.status_code == 404


# ==========================================================
# Password Hashing Test Cases
# ==========================================================

def test_password_is_hashed(client):
    payload = {
        "first_name": "Hash",
        "last_name": "Test",
        "email": "hash_test@example.com",
        "password": "123456"
    }

    response = client.post(
        "/api/v1/users/",
        json=payload
    )

    assert response.status_code == 201

    user = response.json

    # Password must not be returned in the response
    assert "password" not in user


def test_verify_password():
    from app.models.user import User

    user = User(
        first_name="Test",
        last_name="User",
        email="verify@example.com",
        password="temporary"
    )

    user.hash_password("123456")

    assert user.password != "123456"
    assert user.verify_password("123456") is True
    assert user.verify_password("wrong_password") is False
