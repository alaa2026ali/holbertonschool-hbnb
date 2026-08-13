import pytest
import uuid

from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_token(client):
    email = f"test_{uuid.uuid4().hex}@test.com"

    # Create user
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

    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 200

    return response.json["access_token"]

