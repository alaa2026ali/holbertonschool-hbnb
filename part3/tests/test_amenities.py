import pytest
from app import create_app, db
from config import TestingConfig
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()


def get_admin_token(client):
    """Create an admin user and return a JWT token."""

    from app.services import facade

    user = facade.create_user({
        "first_name": "Admin",
        "last_name": "Test",
        "email": "admin_amenity@example.com",
        "password": "123456"
    })

    user.is_admin = True
    db.session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin_amenity@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    return response.json["access_token"]


# ==============================================================================
# 1. LIST & CREATION ENDPOINT TESTS
# ==============================================================================

def test_get_all_amenities_success(client):
    with patch(
        "app.api.v1.amenities.facade.get_all_amenities"
    ) as mock_get_all:

        mock_get_all.return_value = [
            {"id": "amenity-1", "name": "WiFi"},
            {"id": "amenity-2", "name": "Swimming Pool"}
        ]

        response = client.get("/api/v1/amenities/")

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 2
        assert response.json[0]["name"] == "WiFi"


def test_create_amenity_success(client):
    token = get_admin_token(client)

    payload = {
        "name": "Air Conditioning"
    }

    with patch(
        "app.api.v1.amenities.facade.create_amenity"
    ) as mock_create:

        mock_create.return_value = {
            "id": "amenity-3",
            "name": "Air Conditioning"
        }

        response = client.post(
            "/api/v1/amenities/",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        assert response.json["id"] == "amenity-3"
        assert response.json["name"] == "Air Conditioning"


# ==============================================================================
# 2. SPECIFIC AMENITY RESOURCE TESTS
# ==============================================================================

def test_get_amenity_by_id_success(client):
    amenity_id = "amenity-1"

    with patch(
        "app.api.v1.amenities.facade.get_amenity"
    ) as mock_get:

        mock_get.return_value = {
            "id": amenity_id,
            "name": "WiFi"
        }

        response = client.get(
            f"/api/v1/amenities/{amenity_id}"
        )

        assert response.status_code == 200
        assert response.json["id"] == amenity_id
        assert response.json["name"] == "WiFi"


def test_get_amenity_by_id_not_found(client):
    non_existent_id = "missing-id-123"

    with patch(
        "app.api.v1.amenities.facade.get_amenity"
    ) as mock_get:

        mock_get.return_value = None

        response = client.get(
            f"/api/v1/amenities/{non_existent_id}"
        )

        assert response.status_code == 404
        assert "Amenity not found" in response.json.get(
            "message",
            ""
        )


def test_update_amenity_success(client):
    token = get_admin_token(client)

    amenity_id = "amenity-1"

    payload = {
        "name": "High-Speed WiFi"
    }

    with patch(
        "app.api.v1.amenities.facade.get_amenity"
    ) as mock_get, patch(
        "app.api.v1.amenities.facade.update_amenity"
    ) as mock_update:

        mock_get.side_effect = [
            {"id": amenity_id, "name": "WiFi"},
            {"id": amenity_id, "name": "High-Speed WiFi"}
        ]

        response = client.put(
            f"/api/v1/amenities/{amenity_id}",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        assert response.json["name"] == "High-Speed WiFi"


def test_update_amenity_not_found(client):
    token = get_admin_token(client)

    non_existent_id = "missing-id-123"

    payload = {
        "name": "Gym"
    }

    with patch(
        "app.api.v1.amenities.facade.get_amenity"
    ) as mock_get:

        mock_get.return_value = None

        response = client.put(
            f"/api/v1/amenities/{non_existent_id}",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 404
