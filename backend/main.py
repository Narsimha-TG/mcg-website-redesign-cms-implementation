from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="AI-Driven RAG Chatbot API")

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

class ThemeToggle(BaseModel):
    theme_preference: str

# In-memory data store
data_store = [
    {"id": 1, "title": "RAG Accuracy Test", "status": "completed", "score": 0.95, "timestamp": "2023-10-27T10:00:00Z"},
    {"id": 2, "title": "Latency Benchmark", "status": "pending", "score": 0.88, "timestamp": "2023-10-27T11:00:00Z"}
]

current_theme = "light"

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_records": len(data_store), "average_score": sum(d['score'] for d in data_store) / len(data_store) if data_store else 0}

@app.post("/api/reviews")
def submit_review(review: Review):
    data_store.append(review.dict())
    return {"message": "Review submitted successfully", "data": review}

@app.post("/api/theme/toggle")
def toggle_theme(theme: ThemeToggle):
    global current_theme
    current_theme = theme.theme_preference
    return {"theme_preference": current_theme}
