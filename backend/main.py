from fastapi import FastAPI, HTTPException
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

class Task(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    status: str
    score: Optional[float] = None
    timestamp: str = datetime.utcnow().isoformat()
    robot_unit_id: str
    task_type: str
    decision_confidence: float
    execution_time_ms: int

# In-memory storage
tasks = [
    Task(title="Warehouse Sort", status="active", robot_unit_id="R-001", task_type="sorting", decision_confidence=0.98, execution_time_ms=120)
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "peripherals": "online", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_tasks": len(tasks), "avg_confidence": sum(t.decision_confidence for t in tasks) / len(tasks)}

@app.post("/api/reviews")
def submit_review(task_id: str, score: float):
    for task in tasks:
        if task.id == task_id:
            task.score = score
            return {"message": "Review recorded"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/api/tasks/dispatch")
def dispatch_task(task: Task):
    tasks.append(task)
    return {"message": "Task dispatched", "id": task.id}

@app.get("/api/tasks/active")
def get_active_tasks():
    return [t for t in tasks if t.status == "active"]