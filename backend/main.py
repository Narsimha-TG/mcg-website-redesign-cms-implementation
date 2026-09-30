from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Robotics AI Task Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str

class ThemeUpdate(BaseModel):
    theme_preference: str

# In-memory data
db = {
    "reviews": [
        {"id": 1, "title": "Task Alpha", "status": "completed", "score": 0.95, "timestamp": "2023-10-27T10:00:00Z"}
    ],
    "settings": {"theme_preference": "light"}
}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_tasks": len(db["reviews"]), "average_score": 0.95}

@app.post("/api/reviews")
def create_review(review: Review):
    db["reviews"].append(review.dict())
    return review

@app.patch("/api/settings/theme")
def update_theme(settings: ThemeUpdate):
    if settings.theme_preference not in ["light", "dark"]:
        raise HTTPException(status_code=400, detail="Invalid theme")
    db["settings"]["theme_preference"] = settings.theme_preference
    return db["settings"]