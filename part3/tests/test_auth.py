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


def create_test_user(client):
    """Create a test user."""
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Auth",
            "last_name": "Test",
            "email": "auth@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201


# ==========================================================
# Success Test Cases
# ==========================================================

def test_login_success(client):
    create_test_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "auth@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json


# ==========================================================
# Validation Test Cases
# ==========================================================

def test_login_invalid_password(client):
    create_test_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "auth@example.com",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401


def test_login_invalid_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401


def test_login_missing_password(client):
    create_test_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "auth@example.com"
        }
    )

    assert response.status_code == 400


def test_login_missing_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "password": "123456"
        }
    )

    assert response.status_code == 400
