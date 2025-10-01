from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers.books import api_router
from app.routers.auth import auth_router
from app.routers.health import health_router
from app.routers.categories import categories_router
from app.routers.stats import stats_router
from app.routers.ml import ml_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books Scraper API")

app.include_router(api_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(categories_router)
app.include_router(stats_router)
app.include_router(ml_router)
