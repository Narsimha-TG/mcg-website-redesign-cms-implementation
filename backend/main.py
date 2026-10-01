from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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
    id: str = None
    title: str
    status: str
    score: float
    timestamp: str = None

# In-memory seed data
db = [
    {"id": "1", "title": "Pick and Place", "status": "completed", "score": 0.98, "timestamp": "2023-10-27T10:00:00Z"},
    {"id": "2", "title": "Path Planning", "status": "running", "score": 0.85, "timestamp": "2023-10-27T10:05:00Z"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_tasks": len(db), "average_score": sum(d['score'] for d in db) / len(db) if db else 0}

@app.post("/api/reviews", response_model=Review)
def create_review(review: Review):
    review.id = str(uuid.uuid4())
    review.timestamp = datetime.utcnow().isoformat()
    db.append(review.dict())
    return review

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)