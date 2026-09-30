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
    assert "avg_score" in data
    assert isinstance(data["total_tasks"], int)

def test_submit_review():
    payload = {
        "title": "Test Task",
        "status": "pending",
        "score": 0.95
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"
    assert data["score"] == 0.95
    assert "id" in data

def test_get_telemetry():
    response = client.get("/api/telemetry")
    assert response.status_code == 200
    assert isinstance(response.json(), list)