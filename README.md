# Supermarket API

A FastAPI-based backend service for scraping, storing, and serving local supermarket product data in Barbados.

## Features
- Scrapes products from multiple supermarket websites.
- Stores products, supermarkets, and categories in a PostgreSQL database (NeonDB supported).
- Provides REST API routes for:
  - `/products` – Get products with filters (supermarket, category, price range, search, pagination, sorting).
  - `/supermarkets` – Get list of supermarkets.
  - `/categories` – Get list of categories.
- SQLAlchemy ORM for database interaction.
- Pydantic models for validation.

## Project Structure
```
supermarket-api/
│── database/
│   ├── db_setup.py      # Database setup (SQLAlchemy + session)
│   ├── models.py        # SQLAlchemy models (Product, Supermarket, Category)
│── routes/
│   ├── routes_products.py   # Product API routes
│   ├── routes_supermarkets.py # Supermarket API routes
│   ├── routes_categories.py  # Category API routes
│── main.py              # FastAPI entrypoint
│── requirements.txt     # Dependencies
│── .env                 # Environment variables
│── .gitignore           # Git ignore rules
│── README.md            # Project documentation
```

## Scraper

The scraper is responsible for collecting supermarket data (products, categories, and prices) and storing it in the database.

- **Libraries Used**: BeautifulSoup4 & Requests
- **Purpose**: Extracts product listings from supermarket websites and normalizes them into standard categories.
- **Integration**: The scraper writes directly to the PostgreSQL database (NeonDB) so that the API always has fresh data.
- **Pagination Handling**: Automatically follows multiple pages within a category until all products are scraped.
- **Category Mapping**: Supermarket-specific categories are mapped to standardized categories to reduce duplication and ensure consistency.
- **Execution**: Scrapers are run as Python scripts (e.g., `python scraper/aone.py`) and can be extended to additional supermarkets.

Future improvement: Automating scrapers with a scheduler (e.g., Cron jobs, Celery, or FastAPI background tasks).


## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Ranaco-Phillips/supermarket-api.git
cd supermarket-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root:
```
DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

## API Documentation
Interactive docs available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc


## Example API Calls

### Get Products
```
GET /products?supermarket=1&category=2&min_price=5&max_price=20&sort=price_asc&page=1&per_page=10
```

### Get Supermarkets
```
GET /supermarkets
```

### Get Categories
```
GET /categories
```

## Tech Stack
- **FastAPI** – Web framework for building the API
- **SQLAlchemy** – ORM for database interactions
- **PostgreSQL (NeonDB)** – Cloud database
- **Uvicorn** – ASGI server for running FastAPI
- **BeautifulSoup4 & Requests** – Web scraping (used to extract product, category, and supermarket data)

---
Future plans:
- Add user authentication & favorites
- Add price history tracking
- Add caching for faster API responses
