from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="E-commerce SaaS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    id: str
    user_id: str
    status: str
    created_at: datetime

# In-memory seed data
users = {"user_123": {"id": "1", "user_id": "user_123", "status": "active", "created_at": datetime.now()}}

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now()}

@app.post("/api/v1/auth/login")
def login(credentials: dict):
    return {"token": "mock-jwt-token", "user_id": "user_123"}

@app.get("/api/v1/analytics/data")
def get_analytics():
    return {"metrics": [{"source": "api_v1", "value": 100}, {"source": "api_v2", "value": 250}]}

@app.post("/api/v1/subscriptions/checkout")
def create_checkout(data: dict):
    return {"session_id": "cs_test_123", "url": "https://checkout.stripe.com/pay/123"}

@app.get("/api/v1/user/profile")
def get_profile():
    return users.get("user_123")