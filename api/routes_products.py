from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from database.db_setup import get_db
from database.models import Product, Supermarket, Category

router = APIRouter()

@router.get("/")
def get_products(
    supermarket: Optional[int] = Query(None, description="Filter by supermarket ID"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = Query(None, description="Search by product name"),
    sort: Optional[str] = Query(
        None,
        pattern="^(price_asc|price_desc)$", 
        description="Sort by price ascending or descending"
    ),
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get products with filters and pagination (real DB).
    """

    query = (
        db.query(
            Product,
            Supermarket.name.label("supermarket_name"),
            Category.name.label("category_name")
        )
        .join(Supermarket, Product.supermarket_id == Supermarket.id)
        .join(Category, Product.category_id == Category.id)
    )

    # Filters
    if supermarket:
        query = query.filter(Product.supermarket_id == supermarket)
    if category:
        query = query.filter(Product.category_id == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())

    # Pagination
    total = query.count()
    results = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "products": [
            {
                "id": r.Product.id,
                "name": r.Product.name,
                "price": r.Product.price,
                "supermarket_id": r.Product.supermarket_id,
                "supermarket_name": r.supermarket_name, 
                "category_id": r.Product.category_id,
                "category_name": r.category_name,     
                "last_updated": r.Product.last_updated,
            }
            for r in results
        ],
    }


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID with supermarket + category names.
    """
    result = (
        db.query(Product, Supermarket.name.label("supermarket_name"), Category.name.label("category_name"))
        .join(Supermarket, Product.supermarket_id == Supermarket.id)
        .join(Category, Product.category_id == Category.id)
        .filter(Product.id == product_id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    product, supermarket_name, category_name = result

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "supermarket": supermarket_name,
        "category": category_name,
        "last_updated": product.last_updated,
    }