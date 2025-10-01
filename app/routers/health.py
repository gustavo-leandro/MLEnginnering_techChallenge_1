from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

health_router = APIRouter(prefix="/api/v1", tags=["health"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@health_router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": True}
    except Exception:
        return {"status": "error", "db": False}
