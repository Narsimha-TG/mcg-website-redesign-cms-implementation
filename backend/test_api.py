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

def test_create_review():
    payload = {
        "id": 2,
        "title": "Task Beta",
        "status": "pending",
        "score": 0.88,
        "timestamp": "2023-10-27T12:00:00Z"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Task Beta"

def test_update_theme_invalid():
    response = client.patch("/api/settings/theme", json={"theme_preference": "neon"})
    assert response.status_code == 400