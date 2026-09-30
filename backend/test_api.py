from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_reviews():
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review():
    response = client.post("/api/reviews", json={"id": 3, "text": "Amazing speed", "rating": 5})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Amazing speed"

def test_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
