from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Algo Trade Automation API")

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
    "reviews": [{"id": 1, "title": "Strategy Alpha", "status": "active", "score": 95.5, "timestamp": "2023-10-27T10:00:00Z"}],
    "settings": {"theme_preference": "dark"}
}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"metrics": db["reviews"], "count": len(db["reviews"])}

@app.post("/api/reviews")
def create_review(review: Review):
    db["reviews"].append(review.dict())
    return review

@app.patch("/api/ui/theme")
def update_theme(theme: ThemeUpdate):
    db["settings"]["theme_preference"] = theme.theme_preference
    return db["settings"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)