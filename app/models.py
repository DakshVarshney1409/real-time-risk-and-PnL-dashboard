from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

# --- SQLAlchemy Table Model (for the database) ---
class Position(Base):
    """Represents an aggregated equity position in the DB."""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Float, nullable=False)
    average_cost = Column(Float, default=0.0)
    last_update = Column(DateTime, default=datetime.utcnow)
    
    # Risk/PnL fields updated by the quant calculation process
    market_price = Column(Float, default=0.0)
    mtm_pnl = Column(Float, default=0.0)
    historical_var_95 = Column(Float, default=0.0)

# --- Pydantic Schemas (for API request/response validation) ---
class PositionSchema(BaseModel):
    symbol: str
    quantity: float
    average_cost: float
    market_price: float
    mtm_pnl: float
    historical_var_95: float

    class Config:
        orm_mode = True