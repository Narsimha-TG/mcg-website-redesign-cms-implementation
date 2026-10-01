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
    assert "total_tasks" in data
    assert "average_score" in data
    assert isinstance(data["total_tasks"], int)
    assert isinstance(data["average_score"], float)

def test_create_review():
    payload = {
        "title": "Test Automation Task",
        "status": "in-progress",
        "score": 0.92
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == payload["status"]
    assert data["score"] == payload["score"]
    assert "id" in data
    assert "timestamp" in data