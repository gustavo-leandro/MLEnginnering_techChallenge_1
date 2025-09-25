from app.scraping import scrape_books
from app.database import SessionLocal
from app import crud, schemas, scraping
from app.routers.books import search_books

db = scrape_books(pages=1)
print(db)