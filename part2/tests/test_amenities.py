import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configures the Flask test client environment without booting the live server."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ==============================================================================
# 1. LIST & CREATION ENDPOINT TESTS (/api/v1/amenities/)
# ==============================================================================

def test_get_all_amenities_success(client):
    """Ensures the GET endpoint returns a 200 status code and an array of amenities."""
    with patch('app.services.facade.get_all_amenities') as mock_get_all:
        mock_get_all.return_value = [
            {"id": "amenity-1", "name": "WiFi"},
            {"id": "amenity-2", "name": "Swimming Pool"}
        ]
        
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 2
        assert response.json[0]['name'] == "WiFi"

def test_create_amenity_success(client):
    """Ensures a new amenity can be successfully added via a POST request."""
    payload = {
        "name": "Air Conditioning"
    }
    
    with patch('app.services.facade.create_amenity') as mock_create:
        mock_create.return_value = {"id": "amenity-3", "name": "Air Conditioning"}
        
        response = client.post('/api/v1/amenities/', json=payload)
        assert response.status_code == 201
        assert response.json['id'] == "amenity-3"
        assert response.json['name'] == "Air Conditioning"


# ==============================================================================
# 2. SPECIFIC AMENITY RESOURCE TESTS (/api/v1/amenities/<amenity_id>)
# ==============================================================================

def test_get_amenity_by_id_success(client):
    """Ensures a valid amenity ID returns a 200 status code and the item data."""
    amenity_id = "amenity-1"
    
    with patch('app.services.facade.get_amenity') as mock_get:
        mock_get.return_value = {"id": amenity_id, "name": "WiFi"}
        
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        assert response.status_code == 200
        assert response.json['id'] == amenity_id
        assert response.json['name'] == "WiFi"

def test_get_amenity_by_id_not_found(client):
    """Ensures a 404 status code is thrown when an invalid amenity ID is provided."""
    non_existent_id = "missing-id-123"
    
    with patch('app.services.facade.get_amenity') as mock_get:
        mock_get.return_value = None  # Simulates missing object from database
        
        response = client.get(f'/api/v1/amenities/{non_existent_id}')
        assert response.status_code == 404
        assert "Amenity not found" in response.json.get('message', '')

def test_update_amenity_success(client):
    """Ensures an existing amenity updates fields smoothly via a PUT request."""
    amenity_id = "amenity-1"
    payload = {
        "name": "High-Speed WiFi"
    }
    
    with patch('app.services.facade.get_amenity') as mock_get, \
         patch('app.services.facade.update_amenity') as mock_update:
        
        # Mock get_amenity to satisfy the check, then return updated mock payload
        mock_get.side_effect = [
            {"id": amenity_id, "name": "WiFi"},             # First check inside route
            {"id": amenity_id, "name": "High-Speed WiFi"}   # Final return value response
        ]
        
        response = client.put(f'/api/v1/amenities/{amenity_id}', json=payload)
        assert response.status_code == 200
        assert response.json['name'] == "High-Speed WiFi"

def test_update_amenity_not_found(client):
    """Ensures a PUT request on a non-existent ID fails with a 404 status code."""
    non_existent_id = "missing-id-123"
    payload = {
        "name": "Gym"
    }
    
    with patch('app.services.facade.get_amenity') as mock_get:
        mock_get.return_value = None
        
        response = client.put(f'/api/v1/amenities/{non_existent_id}', json=payload)
        assert response.status_code == 404
