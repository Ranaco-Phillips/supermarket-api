from fastapi import FastAPI
from api.routes_products import router as products_router
from api.routes_categories import router as categories_router
from api.routes_supermarkets import router as supermarkets_router
from api.routes_search import router as search_router

app = FastAPI(title="Supermarket API")

@app.get("/")
def read_root():
    return {"message": "FastAPI + Neon PostgreSQL is working 🚀"}

# Register routes
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(supermarkets_router, prefix="/supermarkets", tags=["Supermarkets"])
app.include_router(search_router, prefix="/search", tags=["Search"])

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
