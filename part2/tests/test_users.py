import pytest
from run import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ==========================================================
# Success Test Cases
# ==========================================================

def test_create_user_success(client):
    payload = {
        "first_name": "Fahad",
        "last_name": "Alotaibi",
        "email": "fahad_test@example.com"
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
        "email": "abc"
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_empty_first_name(client):
    payload = {
        "first_name": "",
        "last_name": "Test",
        "email": "test@example.com"
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_long_first_name(client):
    payload = {
        "first_name": "A" * 51,
        "last_name": "Test",
        "email": "long@example.com"
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400


def test_create_user_missing_last_name(client):
    payload = {
        "first_name": "Ali",
        "email": "ali@example.com"
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

    response = client.put("/api/v1/users/non_existing_id", json=payload)

    assert response.status_code == 404
