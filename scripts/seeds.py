# scripts/seeds.py
from sqlalchemy.orm import Session
from database.db_setup import engine, Base, SessionLocal
from database.models import Supermarket, Category
from config.categories import STANDARD_CATEGORIES

def seed_supermarkets(session: Session):
    supermarkets = [
        {"name": "A1 Supermarket", "website": "https://aonesupermarkets.com"},
        {"name": "Massy Stores", "website": "https://www.shopmassystoresbb.com"},
        {"name": "Cost.U.Less", "website": "https://www.shopcostuless.com"},
    ]

    for market in supermarkets:
        exists = session.query(Supermarket).filter_by(name=market["name"]).first()
        if not exists:
            session.add(Supermarket(name=market["name"], website=market["website"]))
    session.commit()
    print("Supermarkets seeded.")
    

def seed_categories(session: Session):
    # STANDARD_CATEGORIES should be a dict like: {"bakery": "Bakery", "beverages": "Beverages"}
    for slug, name in STANDARD_CATEGORIES.items():
        exists = session.query(Category).filter_by(slug=slug).first()
        if not exists:
            session.add(Category(name=name, slug=slug))
    session.commit()
    print("Categories seeded.")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    db = SessionLocal()

    seed_supermarkets(db)
    seed_categories(db)

    db.close()
