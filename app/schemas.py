"""
Schemas Pydantic para validação e serialização dos dados de livros.
"""
from pydantic import BaseModel

class BookBase(BaseModel):
	"""
	Schema base para livro, usado em criação e leitura.
	"""
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
