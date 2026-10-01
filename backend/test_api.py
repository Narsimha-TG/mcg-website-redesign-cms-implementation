import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_analytics():
    response = client.get("/api/v1/analytics/data")
    assert response.status_code == 200
    assert "metrics" in response.json()
    assert len(response.json()["metrics"]) > 0

def test_create_checkout():
    payload = {"price_id": "price_123", "quantity": 1}
    response = client.post("/api/v1/subscriptions/checkout", json=payload)
    assert response.status_code == 200
    assert "session_id" in response.json()
    assert response.json()["session_id"] == "cs_test_123"

def test_login():
    payload = {"username": "testuser", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()