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
    data = response.json()
    assert "metrics" in data
    assert isinstance(data["metrics"], list)

def test_create_review():
    payload = {
        "id": 2,
        "title": "Strategy Beta",
        "status": "active",
        "score": 88.0,
        "timestamp": "2023-10-28T12:00:00Z"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_update_theme():
    payload = {"theme_preference": "light"}
    response = client.patch("/api/ui/theme", json=payload)
    assert response.status_code == 200
    assert response.json()["theme_preference"] == "light"