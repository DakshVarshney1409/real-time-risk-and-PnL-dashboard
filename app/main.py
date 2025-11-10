from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from .database import create_db_and_tables, get_db
from .models import Position, PositionSchema
import asyncio
import json
import random
from typing import List

app = FastAPI()
create_db_and_tables() # Initialize tables on startup

# Global list of active WebSocket clients and connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            # We use try/except to handle clients that might disconnect mid-broadcast
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()


# --- REST API Endpoint (Position Data) ---
@app.get("/positions", response_model=List[PositionSchema])
def get_all_positions(db: Session = Depends(get_db)):
    """Fetches all equity positions."""
    positions = db.query(Position).all()
    if not positions:
        # Add a dummy position if the table is empty for easy testing
        if not db.query(Position).first():
            db_position = Position(
                symbol="AAPL",
                quantity=100.0,
                average_cost=150.0,
                market_price=150.0
            )
            db.add(db_position)
            db.commit()
            db.refresh(db_position)
            return [db_position]
        raise HTTPException(status_code=404, detail="No positions found")
    return positions


# --- WebSocket Endpoint (Real-Time Market Data) ---
@app.websocket("/ws/market_data")
async def websocket_endpoint(websocket: WebSocket):
    """Handles real-time market data connection."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive, client can send messages if needed
            # For this project, we primarily send data from the server.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client disconnected: {websocket.client}")


# --- Background Task (Simulate Real-Time Price Updates) ---
async def market_data_simulator():
    """A background task that simulates real-time price changes and broadcasts them."""
    while True:
        # 1. Fetch all symbols we care about
        with get_db() as db:
            symbols = [p.symbol for p in db.query(Position.symbol).all()]

        # 2. Generate and broadcast a random price update
        if symbols:
            symbol = random.choice(symbols)
            # Simulate a small random price fluctuation around $100-$200
            price_change = random.uniform(-0.5, 0.5)
            new_price = round(db.query(Position.market_price).filter(Position.symbol == symbol).first()[0] + price_change, 2)
            
            update_data = {
                "symbol": symbol,
                "price": new_price,
                "timestamp": datetime.now().isoformat()
            }
            
            # Send data to all connected clients
            await manager.broadcast(json.dumps(update_data))

            # Update the DB (this is where the quant calculation logic would typically run)
            with get_db() as db_update:
                position_to_update = db_update.query(Position).filter(Position.symbol == symbol).first()
                if position_to_update:
                    # In a real system, a separate quant service would calculate PnL/VaR
                    # For now, we update the price directly.
                    position_to_update.market_price = new_price
                    db_update.commit()


        await asyncio.sleep(0.5) # Send an update every 0.5 seconds

@app.on_event("startup")
async def startup_event():
    """Start the background simulator on FastAPI startup."""
    asyncio.create_task(market_data_simulator())

# To run the app: uvicorn app.main:app --reload