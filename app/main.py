from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers.books import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books Scraper API")

app.include_router(api_router)
