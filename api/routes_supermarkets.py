from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db_setup import get_db
from database.models import Supermarket

router = APIRouter()

# Get all supermarkets
@router.get("/supermarkets")
def get_supermarkets(db: Session = Depends(get_db)):
    return db.query(Supermarket).all()

# Get supermarket by ID
@router.get("/supermarkets/{supermarket_id}")
def get_supermarket(supermarket_id: int, db: Session = Depends(get_db)):
    supermarket = db.query(Supermarket).filter(Supermarket.id == supermarket_id).first()
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    return supermarket

# Create a new supermarket
@router.post("/supermarkets")
def create_supermarket(name: str, db: Session = Depends(get_db)):
    supermarket = Supermarket(name=name)
    db.add(supermarket)
    db.commit()
    db.refresh(supermarket)
    return supermarket
