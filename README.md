# Books Scraper API

## Project Overview

Books Scraper API is an application developed with FastAPI that performs web scraping of books from [Books to Scrape](https://books.toscrape.com/), stores data in a PostgreSQL database (via Supabase), and exposes a complete REST API for querying, analysis, and integration with Machine Learning models.

The project also includes:
* JWT Authentication
* SQLAlchemy ORM
* Structured logging
* Interactive Streamlit dashboard for log visualization and statistics analysis

GitHub Repository: [gustavo-leandro/MLEnginnering_techChallenge_1](https://github.com/gustavo-leandro/MLEnginnering_techChallenge_1.git)  
Production API: [https://gleandro-book-api-996cbfb885c8.herokuapp.com/](https://gleandro-book-api-996cbfb885c8.herokuapp.com/)

## Architecture Overview

| Component | Description |
|------------|-------------|
| FastAPI | Main web framework for building the API endpoints |
| SQLAlchemy | ORM for defining database models and executing queries |
| PostgreSQL (Supabase) | Cloud database for persistent storage |
| JWT Authentication | Secure access control for protected routes |
| Modular Routers | Separation of concerns between API modules |
| Structured Logging | All HTTP requests are logged in the database |
| Streamlit | Dashboard for analytics and monitoring |

## Architectural Plan

### Data Pipeline

The system follows a complete data pipeline from ingestion to consumption, designed for modularity, scalability, and ML integration.

1. **Data Ingestion:**  
   The scraping module extracts information from [books.toscrape.com](https://books.toscrape.com/), collecting attributes such as title, category, price, and rating.

2. **Processing and Storage:**  
   Data is processed and stored in a **PostgreSQL** database hosted on **Supabase**, using **SQLAlchemy** for ORM mapping and queries. Each scraping execution is logged for traceability and reproducibility.

3. **API Exposure:**  
   The **FastAPI** application exposes RESTful endpoints organized by responsibility. All routes use **JWT authentication**, and every HTTP request is logged in structured form for analysis through the **Streamlit** dashboard.

4. **Data Consumption:**  
   Data scientists can directly consume structured datasets from the `/api/v1/ml/features` and `/api/v1/ml/training-data` endpoints, enabling analytical workflows and machine learning experiments.

### Architecture and Scalability

The architecture was designed with maintainability and future scalability in mind:

* **Independent modules:** scraping, API, authentication, monitoring, and ML components are decoupled.  
* **Scalable storage:** **Supabase** supports horizontal scaling and replication.  
* **Containerization-ready:** easily deployable via **Docker** and orchestrated with **Kubernetes** or serverless platforms.  
* **Observability:** structured logs can be integrated with monitoring tools such as **Prometheus**, **Grafana**, or **DataDog**.

### Data Science and ML Use Case

The project provides a structured and reliable data foundation for analytics and machine learning:

* Dedicated endpoints for retrieving ML-ready features and training samples.  
* Easy integration with **Jupyter notebooks** or **MLOps pipelines**.  
* Ideal for developing models for recommendation, price prediction, or rating analysis.  
* Predictions can be submitted back to the API for evaluation and tracking.

### Machine Learning Integration Plan

The ML module was designed for incremental integration and deployment:

1. **Feature export:** available through `/api/v1/ml/features` in JSON format.  
2. **External training:** models can be trained externally and versioned independently.  
3. **Model deployment:** trained models can be integrated into the API with dedicated inference endpoints.  
4. **Monitoring and metrics:** model performance and logs can be tracked using **Streamlit** or external observability tools.

## Installation and Setup

### 1. Clone the repository

```

git clone https://github.com/gustavo-leandro/MLEnginnering_techChallenge_1.git
cd MLEnginnering_techChallenge_1

```

### 2. Install dependencies (Python 3.12+)

```

poetry install

```

### 3. Configure the database

1. Create a project on Supabase and obtain the PostgreSQL connection string.
2. In the `app/database.py` file, define the URL:
```

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@host:port/dbname"

```
3. Install the PostgreSQL driver:
```

poetry add psycopg2-binary

```

### 4. Environment variables (optional)

Configure your credentials and secrets in the `.env` file.

## API Routes Documentation

The API follows a RESTful structure organized into modules.

### Authentication

| Method | Route | Description |
|--------|------|------------|
| POST | `/api/v1/auth/login` | Authentication via username and password |
| POST | `/api/v1/auth/refresh` | Generate new JWT token |

### Books

| Method | Route | Description |
|--------|------|------------|
| GET | `/api/v1/books/` | List books (paginated) |
| POST | `/api/v1/books/scraping/trigger` | Execute scraping and save to database |
| GET | `/api/v1/books/search` | Search books by title or category |
| GET | `/api/v1/books/top-rated` | List top-rated books |
| GET | `/api/v1/books/price-range` | Search books by price range |
| GET | `/api/v1/books/{id}` | Get book by ID |

### Categories

| Method | Route | Description |
|--------|------|------------|
| GET | `/api/v1/categories` | List all categories |

### Health

| Method | Route | Description |
|--------|------|------------|
| GET | `/api/v1/health` | Check API and database status |

### Stats

| Method | Route | Description |
|--------|------|------------|
| GET | `/api/v1/stats/overview` | General book statistics |
| GET | `/api/v1/stats/categories` | Statistics by category |
| GET | `/api/v1/stats/top-rated` | Top-rated books |
| GET | `/api/v1/stats/price-range` | Books within a price range |

### Machine Learning

| Method | Route | Description |
|--------|------|------------|
| GET | `/api/v1/ml/features` | Returns features for ML use |
| GET | `/api/v1/ml/training-data` | Returns random sample of 100 books |
| POST | `/api/v1/ml/predictions` | Submit data and return predictions (authenticated) |

## Example Requests and Responses

### Login

```

POST /api/v1/auth/login
Content-Type: application/json

{
"username": "admin",
"password": "admin"
}

```

**Response:**
```

{
"access_token": "eyJhbGciOi...",
"token_type": "bearer"
}

```

## Running the Application

### Local

```

poetry run uvicorn app.main:app --reload

```

Access the API at:  
[http://localhost:8000](http://localhost:8000)

Interactive documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Streamlit Dashboard

```

streamlit run dashboard.py

```

Available at:  
[http://localhost:8501](http://localhost:8501)

## Deployed Version

The production version is available at:  
[https://gleandro-book-api-996cbfb885c8.herokuapp.com/](https://gleandro-book-api-996cbfb885c8.herokuapp.com/)

## Additional Notes

* All HTTP requests are logged in the `request_logs` table.
* In production, use environment variables for secrets and connections.
* The scraping logic is adapted for books.toscrape.com and can be adjusted for other sources.
* ML endpoints are ready for integration with custom models.

## License

This project is distributed under the GNU General Public License v3.0 (GPL-3.0). You may redistribute and/or modify this software under the terms of the GPL-3.0, as published by the Free Software Foundation.