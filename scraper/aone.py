import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session

from config.aone_categories import AONE_BASE_URL, AONE_CATEGORIES
from database.db_setup import SessionLocal
from database.models import Supermarket, Category, Product


# def scrape_paginated_category(start_url: str, category: str = "General"):
def scrape_paginated_category(session: Session, supermarket_id: int, category_id: int, start_url: str):
    """
    Scrape all pages of a single category from AOne supermarket.
    Handles pagination until no more pages exist.
    """
    url = start_url
    new_products = []
    

    while url:
        print(f"Scraping: {url} (Category ID: {category_id})")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        product_containers = soup.select(".card__title")

        for product in product_containers:
            name = product.get_text(strip=True)

            parent = product.parent
            price_tag = parent.select_one(".product-card__price")
            price_raw = price_tag.get_text(strip=True) if price_tag else "N/A"

           # Extract the first number from the raw price string
            price = None
            if price_raw != "N/A":
                match = re.search(r"\d+(\.\d+)?", price_raw)  # matches "4.25" or "10"
                if match:
                    price = float(match.group())


           # Check if product already exists (optional)
            existing = session.query(Product).filter_by(
                name=name, supermarket_id=supermarket_id, category_id=category_id
            ).first()
            if existing:
                # Optionally, update price or last_updated
                existing.price = price
                existing.last_updated = datetime.utcnow()
                session.add(existing)
            else:
                # Insert new product
                db_product = Product(
                    name=name,
                    price=price,
                    last_updated=datetime.utcnow(),
                    supermarket_id=supermarket_id,
                    category_id=category_id,
                )
                session.add(db_product)
                new_products.append(db_product)

        # Commit after each page to avoid too many uncommitted objects
        session.commit()

        # Look for next page
        next_page_tag = soup.select_one("a.pagination__arrow--next")
        if next_page_tag and "href" in next_page_tag.attrs:
            url = "https://aonesupermarkets.com" + next_page_tag["href"]
        else:
            url = None  # stop loop

    
    return new_products


def scrape_all_categories():
    """
    Scrape multiple categories for AOne.
    """
    db = SessionLocal()

    # Lookup AOne supermarket from DB
    supermarket = db.query(Supermarket).filter_by(name="A1 Supermarket").first()
    if not supermarket:
        raise ValueError("Supermarket 'AOne' not found in database. Seed it first!")

    
    for slug, category_name in AONE_CATEGORIES.items():

        #Look up the category in the DB
        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            print(f"Category '{category_name}' not found in DB. Skipping...")
            continue

        # Build the category url
        start_url = AONE_BASE_URL + slug

        #Scrape all pages of the selected category
        scrape_paginated_category(db, supermarket.id, category.id, start_url)
        

    db.close()


if __name__ == "__main__":
    scrape_all_categories()
    print("\n Scraping completed and products saved to the database.")

# def scrape_all_categories(categories: list):
#     """
#     Scrape multiple categories, each with pagination.
#     categories: list of tuples [(url, category_name), ...]
#     """
#     all_products = []
#     for url, category in categories:
#         category_products = scrape_paginated_category(url, category)
#         all_products.extend(category_products)

#     return all_products


# if __name__ == "__main__":
#     # Build urls_to_scrape dynamically from config
#     urls_to_scrape = [(AONE_BASE_URL + slug, name) for slug, name in AONE_CATEGORIES.items()]

#     products = scrape_all_categories(urls_to_scrape)

#     print(f"\n Total products scraped: {len(products)}\n")
#     for p in products[:10]:
#         print(p)