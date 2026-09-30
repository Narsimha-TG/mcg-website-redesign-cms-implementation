from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import uuid

app = FastAPI(title="Robotics AI Task Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    title: str
    status: str
    score: float

# In-memory storage
db = {
    "tasks": [
        {"id": "1", "title": "Pick and Place", "status": "completed", "score": 0.98, "timestamp": "2023-10-27T10:00:00Z", "telemetry_data": {"battery": 85, "temp": 42}},
        {"id": "2", "title": "Path Planning", "status": "running", "score": 0.85, "timestamp": "2023-10-27T10:05:00Z", "telemetry_data": {"battery": 82, "temp": 45}}
    ]
}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_tasks": len(db["tasks"]), "avg_score": sum(t["score"] for t in db["tasks"]) / len(db["tasks"])}

@app.post("/api/reviews")
def submit_review(review: Review):
    new_task = {
        "id": str(uuid.uuid4()),
        "title": review.title,
        "status": review.status,
        "score": review.score,
        "timestamp": datetime.utcnow().isoformat(),
        "telemetry_data": {}
    }
    db["tasks"].append(new_task)
    return new_task

@app.get("/api/telemetry")
def get_telemetry():
    return [{"id": t["id"], "telemetry_data": t["telemetry_data"]} for t in db["tasks"]]