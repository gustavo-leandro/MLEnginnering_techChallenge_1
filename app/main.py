
"""
Main entry point for the Books Scraper API.
Initializes FastAPI app, includes routers, and sets up request logging middleware.
"""

import time
import jwt
from fastapi import FastAPI, Request
from starlette.responses import Response as StarletteResponse
from app.database import engine, SessionLocal
from app import models
from app.crud import create_request_log
from app.routers.books import api_router
from app.routers.auth import auth_router
from app.routers.health import health_router
from app.routers.categories import categories_router
from app.routers.stats import stats_router
from app.routers.ml import ml_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Books Scraper API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all HTTP requests and responses, including timing.
    Persists log to database even on error.
    """
    start_time = time.time()
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        response = StarletteResponse("Internal Server Error", status_code=500)
    duration_ms = (time.time() - start_time) * 1000
    db = SessionLocal()
    try:
        create_request_log(
            db=db,
            http_method=request.method,
            endpoint=request.url.path,
            status_code=status_code,
            duration_ms=duration_ms
        )
    finally:
        db.close()
    return response


app.include_router(api_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(categories_router)
app.include_router(stats_router)
app.include_router(ml_router)
