from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Robotics AI Task Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RobotTask(BaseModel):
    id: str = None
    title: str
    status: str
    score: float
    timestamp: str = None
    confidence_level: float
    action_taken: str

# In-memory store
db = [
    {"id": "1", "title": "Pick and Place", "status": "completed", "score": 0.98, "timestamp": "2023-10-27T10:00:00Z", "confidence_level": 0.99, "action_taken": "move_arm_to_bin"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_tasks": len(db), "avg_score": sum(t['score'] for t in db) / len(db) if db else 0}

@app.post("/api/reviews")
def submit_review(task: RobotTask):
    task.id = str(uuid.uuid4())
    task.timestamp = datetime.utcnow().isoformat()
    db.append(task.dict())
    return task

@app.post("/api/robot/command")
def execute_command(command: dict):
    return {"status": "success", "executed": command.get("action"), "timestamp": datetime.utcnow().isoformat()}

@app.websocket("/api/logs/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"message": "Connected to AI Decision Stream"})
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass