
"""
Health router: Endpoint for health check of API and database.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

health_router = APIRouter(prefix="/api/v1", tags=["health"])

def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@health_router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for API and database connection.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": True}
    except Exception:
        return {"status": "error", "db": False}
