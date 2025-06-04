import pytest
from fastapi.testclient import TestClient

def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_db_status(client):
    """Test the database status endpoint."""
    response = client.get("/db-status")
    assert response.status_code == 200
    assert "status" in response.json()