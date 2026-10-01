import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_fetch_data():
    response = client.get("/api/data/fetch")
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

def test_toggle_theme_success():
    payload = {"user_id": 101, "theme_preference": "dark"}
    response = client.post("/api/theme/toggle", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["new_theme"] == "dark"

def test_chat_query():
    payload = {"user_id": 101, "message": "Hello AI"}
    response = client.post("/api/chat/query", json=payload)
    assert response.status_code == 200
    assert "ai_response_payload" in response.json()
    assert "AI processed" in response.json()["ai_response_payload"]