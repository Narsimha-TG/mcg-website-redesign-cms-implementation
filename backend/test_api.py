import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_leads" in data
    assert "avg_score" in data

def test_submit_review():
    payload = {"rating": 5, "comment": "Great service"}
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_capture_lead():
    new_lead = {
        "id": "2",
        "title": "Global Solutions",
        "status": "pending",
        "score": 92.0,
        "timestamp": "2023-10-28T12:00:00Z",
        "lead_source": "email",
        "conversion_probability": 0.88
    }
    response = client.post("/api/leads/capture", json=new_lead)
    assert response.status_code == 200
    assert response.json()["status"] == "created"
    assert response.json()["id"] == "2"