from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserTheme(BaseModel):
    user_id: int
    theme_preference: str

class ChatQuery(BaseModel):
    user_id: int
    message: str

# In-memory store
db = [
    {"id": 1, "user_id": 101, "theme_preference": "light", "ai_response_payload": "Hello!", "created_at": datetime.now().isoformat()}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/theme/toggle")
def toggle_theme(data: UserTheme):
    for record in db:
        if record["user_id"] == data.user_id:
            record["theme_preference"] = data.theme_preference
            return {"status": "success", "new_theme": data.theme_preference}
    return {"status": "error", "message": "User not found"}

@app.post("/api/chat/query")
def chat_query(query: ChatQuery):
    # Mock AI integration
    response = f"AI processed: {query.message}"
    return {"user_id": query.user_id, "ai_response_payload": response}

@app.get("/api/data/fetch")
def fetch_data():
    return {"data": db}
