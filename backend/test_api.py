import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review():
    payload = {
        "title": "Test Integration Review",
        "status": "pending",
        "score": 9.5
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data

def test_approve_milestone_not_found():
    payload = {
        "id": "non-existent-id",
        "verification_token": "secret-token"
    }
    response = client.post("/api/milestone/approve", json=payload)
    assert response.status_code == 404