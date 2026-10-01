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

class Trade(BaseModel):
    trade_id: str
    symbol: str
    pattern_type: str
    entry_price: float
    exit_price: float
    timestamp: str
    pnl_impact: float
    status: str

class ConfigUpdate(BaseModel):
    risk_limit: float
    strategy_enabled: bool

# In-memory seed data
trade_db = [
    Trade(trade_id="T1", symbol="BTC/USD", pattern_type="Bullish Engulfing", entry_price=50000.0, exit_price=51000.0, timestamp=datetime.utcnow().isoformat(), pnl_impact=1000.0, status="closed")
]

@app.get("/api/v1/health")
def health_check():
    return {"status": "online", "latency_ms": 2}

@app.get("/api/v1/market-data/stream")
def get_market_data():
    return {"message": "WebSocket connection established", "stream_url": "ws://localhost:8000/ws/market"}

@app.post("/api/v1/strategy/execute")
def execute_strategy(action: dict):
    return {"status": "success", "action_received": action}

@app.get("/api/v1/trades/history", response_model=List[Trade])
def get_history():
    return trade_db

@app.post("/api/v1/config/update")
def update_config(config: ConfigUpdate):
    return {"status": "updated", "new_config": config.dict()}
