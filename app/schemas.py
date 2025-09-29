"""
Schemas Pydantic para validação e serialização dos dados de livros.
"""
from pydantic import BaseModel
from typing import Dict

class ScrapeResponse(BaseModel):
    inserted: int

class BookBase(BaseModel):
    id: int | None = None
    title: str
    category: str
    rating: int
    description: str
    upc: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    num_available: int
    num_reviews: int
    image_url: str
    class Config:
        from_attributes = True

class BookCreate(BookBase):
	"""
	Schema para criação de livro (herda de BookBase).
	"""
	pass

# class BookRead(BaseModel):
#     id: int
#     title: str

class BookStatsOverview(BaseModel):
    total_books: int
    average_price: float
    rating_distribution: Dict[int, int] = {
        "1": 10,
        "2": 5,
        "3": 20,
        "4": 15,
        "5": 50
    }

class BookStatsCategory(BaseModel):
    category: str
    total_books: int
    average_price: float