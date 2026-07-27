import pytest

from app import create_app
from app.services import facade


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    # create user
    client.post(
        "/api/v1/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com",
            "password": "123456"
        }
    )

    # login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )

    return response.json["access_token"]
