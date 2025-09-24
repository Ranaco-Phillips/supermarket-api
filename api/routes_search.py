from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def search_products(q: str, supermarket: str = None, category: str = None):
    """
    Search products by keyword.
    """
    return {
        "query": q,
        "supermarket": supermarket,
        "category": category,
        "results": []
    }
