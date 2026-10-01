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
    assert "total_records" in data
    assert "average_score" in data
    assert isinstance(data["total_records"], int)

def test_submit_review():
    payload = {
        "id": 3,
        "title": "Integration Test Review",
        "status": "completed",
        "score": 0.92,
        "timestamp": "2023-10-27T12:00:00Z"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Review submitted successfully"
    assert response.json()["data"]["id"] == 3

def test_toggle_theme():
    payload = {"theme_preference": "dark"}
    response = client.post("/api/theme/toggle", json=payload)
    assert response.status_code == 200
    assert response.json()["theme_preference"] == "dark"