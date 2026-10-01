from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Robinhood Day-Trading Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    order_id: str = None
    symbol: str
    side: str
    quantity: int
    price: float
    status: str = "pending"
    timestamp: str = None

# In-memory data store
orders_db = []
strategy_enabled = False

@app.get("/api/v1/health")
def health_check():
    return {"status": "online", "auth": "connected"}

@app.get("/api/v1/portfolio")
def get_portfolio():
    return {"balance": 25000.00, "positions": [{"symbol": "AAPL", "qty": 10}]}

@app.post("/api/v1/orders")
def create_order(order: Order):
    order.order_id = str(uuid.uuid4())
    order.timestamp = datetime.utcnow().isoformat()
    orders_db.append(order)
    return order

@app.get("/api/v1/market-data")
def get_market_data():
    return {"symbol": "AAPL", "price": 150.25, "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/strategy/toggle")
def toggle_strategy(enabled: bool = Body(..., embed=True)):
    global strategy_enabled
    strategy_enabled = enabled
    return {"strategy_enabled": strategy_enabled}
