from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from contextlib import contextmanager
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "quant_dashboard.db") 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Initializes the database schema."""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    """Dependency for getting a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
