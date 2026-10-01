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
    assert "total_items" in data
    assert "average_score" in data

def test_submit_review():
    payload = {
        "id": "3",
        "title": "Test Content",
        "status": "published",
        "score": 92.0,
        "timestamp": "2023-10-27T10:00:00",
        "metadata": {"author": "QA"}
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Review submitted successfully"
    
    # Verify it was added
    get_response = client.get("/api/content")
    assert any(item["id"] == "3" for item in get_response.json())