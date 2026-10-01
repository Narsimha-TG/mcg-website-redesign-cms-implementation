import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_reel_success():
    payload = {"prompt": "A futuristic city in the rain"}
    response = client.post("/api/v1/generate-reel", json=payload)
    assert response.status_code == 202
    assert "job_id" in response.json()
    assert response.json()["status"] == "processing"

def test_get_status_not_found():
    response = client.get("/api/v1/status/non-existent-id")
    assert response.status_code == 404

def test_n8n_webhook_update():
    # First create a job
    create_resp = client.post("/api/v1/generate-reel", json={"prompt": "test"})
    job_id = create_resp.json()["job_id"]
    
    # Simulate n8n webhook
    webhook_payload = {
        "job_id": job_id,
        "status": "completed",
        "video_url": "https://storage.com/video.mp4",
        "metadata": {"duration": 15}
    }
    webhook_resp = client.post("/api/v1/webhook/n8n", json=webhook_payload)
    assert webhook_resp.status_code == 200
    
    # Verify status update
    status_resp = client.get(f"/api/v1/status/{job_id}")
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["status"] == "completed"
    assert data["video_url"] == "https://storage.com/video.mp4"