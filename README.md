# Books Scraper API

## Project Description

Books Scraper API is a FastAPI-based application designed to scrape book data from books.toscrape.com, store it in a PostgreSQL (Supabase) database, and provide a robust REST API for querying, analytics, and machine learning consumption. The project follows best practices in Python backend development, including modular routers, JWT authentication, SQLAlchemy ORM, and structured logging of all HTTP requests. A Streamlit dashboard is included for log analytics.

### Architecture Overview

- FastAPI: Main web framework for API endpoints
- SQLAlchemy: ORM for database models and queries
- PostgreSQL (Supabase): Cloud database for persistent storage
- JWT Authentication: Secure access to protected routes
- Routers: Modular separation of API endpoints by responsibility
- Structured Logging: All HTTP requests are logged in the database
- Streamlit: Dashboard for log analytics and monitoring

## Installation and Configuration

1. Clone the repository
	 ```sh
	 git clone https://github.com/yourusername/yourrepo.git
	 cd yourrepo
	 ```

2. Install dependencies (requires Python 3.12+)
	 ```sh
	 poetry install
	 ```

3. Configure the database
	 - Create a project in Supabase and obtain the PostgreSQL connection string.
	 - Edit `app/database.py` and set:
		 ```python
		 SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@host:port/dbname"
		 ```
	 - Install the PostgreSQL driver:
		 ```sh
		 poetry add psycopg2-binary
		 ```

4. Environment variables (optional)
	 - You may use environment variables for secrets and connection strings. See `.env.example` for reference.

## API Routes Documentation

### Authentication

- POST /api/v1/auth/login
	- Request: `{ "username": "admin", "password": "admin" }`
	- Response: `{ "access_token": "...", "token_type": "bearer" }`

- POST /api/v1/auth/refresh
	- Request: Bearer token in Authorization header
	- Response: `{ "access_token": "...", "token_type": "bearer" }`

### Books

- GET /api/v1/books/
	- List books with pagination
	- Query params: `skip`, `limit`
	- Response: List of book objects

- POST /api/v1/books/scraping/trigger
	- Scrape books and save to database (protected)
	- Request: `{ "pages": 2 }`
	- Response: `{ "inserted": 40 }`

- GET /api/v1/books/search
	- Search books by title and/or category
	- Query params: `title`, `category`
	- Response: List of book objects

- GET /api/v1/books/top-rated
	- List books with top rating
	- Response: List of book objects

- GET /api/v1/books/price-range
	- Search books by price range
	- Query params: `min`, `max`
	- Response: List of book objects

- GET /api/v1/books/{id}
	- Get book by ID
	- Response: Book object

### Categories

- GET /api/v1/categories
	- List all book categories
	- Response: List of strings

### Health

- GET /api/v1/health
	- Health check for API and database
	- Response: `{ "status": "ok", "db": true }`

### Stats

- GET /api/v1/stats/overview
	- Get overview statistics for books
	- Response: `{ "total_books": 100, "avg_price": 25.0, "rating_distribution": {"1": 5, "2": 10, ...} }`

- GET /api/v1/stats/categories
	- Get statistics by book category
	- Response: List of category stats

- GET /api/v1/stats/top-rated
	- Get books with top rating
	- Response: List of book objects

- GET /api/v1/stats/price-range
	- Get books within a price range
	- Query params: `min`, `max`
	- Response: List of book objects

### Machine Learning

- GET /api/v1/ml/features
	- Get ML features for all books
	- Response: List of feature objects

- GET /api/v1/ml/training-data
	- Get a random subset of 100 books for ML training
	- Response: List of book objects

- POST /api/v1/ml/predictions
	- Post data for ML predictions (protected)
	- Request: List of feature dicts
	- Response: `{ "predictions": [ { "input": {...}, "prediction": 1 }, ... ] }`

## Example Requests and Responses

### Authentication

Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
	"username": "admin",
	"password": "admin"
}
```
Response:
```json
{
	"access_token": "eyJ...",
	"token_type": "bearer"
}
```

Refresh Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer eyJ...
```
Response:
```json
{
	"access_token": "eyJ...",
	"token_type": "bearer"
}
```

### Books

List Books
```http
GET /api/v1/books/?skip=0&limit=10
```
Response:
```json
[
	{
		"id": 1,
		"title": "Book Title",
		"category": "Fiction",
		"rating": 4,
		"description": "...",
		"upc": "...",
		"product_type": "...",
		"price_excl_tax": 20.0,
		"price_incl_tax": 22.0,
		"tax": 2.0,
		"num_available": 5,
		"num_reviews": 10,
		"image_url": "..."
	},
	...
]
```

Scrape and Save Books
```http
POST /api/v1/books/scraping/trigger
Authorization: Bearer eyJ...
Content-Type: application/json

{
	"pages": 2
}
```
Response:
```json
{
	"inserted": 40
}
```

## Running the Application

1. Start the FastAPI server
	 ```sh
	 poetry run uvicorn app.main:app --reload
	 ```
	 The API will be available at http://localhost:8000.

2. Access the interactive API docs
	 - Swagger UI: http://localhost:8000/docs
	 - Redoc: http://localhost:8000/redoc

3. Run the Streamlit dashboard
	 ```sh
	 streamlit run streamlit/logs_dashboard.py
	 ```
	 The dashboard will be available at http://localhost:8501.

## Additional Notes

- All HTTP requests are logged in the request_logs table for analytics and monitoring.
- For production, configure secrets and connection strings via environment variables.
- The scraping logic is tailored for books.toscrape.com and may require adjustments for other sources.
- Machine learning endpoints are ready for integration with your models.