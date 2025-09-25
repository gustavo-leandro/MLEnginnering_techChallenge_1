"""
Schemas Pydantic para validação e serialização dos dados de livros.
"""
from pydantic import BaseModel

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

class BookRead(BookBase):
	"""
	Schema para leitura de livro, incluindo o ID.
	"""
	id: int
