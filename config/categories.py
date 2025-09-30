# config/categories.py

STANDARD_CATEGORIES = {
    "bakery": "Bakery & Bread",
    "beverages": "Beverages",
    "dairy-eggs": "Dairy & Eggs",
    "frozen": "Frozen Foods",
    "meat-seafood": "Meat & Seafood",
    "produce": "Fruits & Vegetables",
    "grocery": "Pantry Staples & Dry Goods",
    "snacks": "Snacks & Confectionery",
    "condiments-sauces": "Condiments, Sauces & Spices",
    "breakfast-cereal": "Breakfast & Cereal",
    "household": "Household Essentials",
    "personal-care": "Personal Care & Health",
    "baby": "Baby Products",
    "pet": "Pet Supplies",
    "alcohol": "Beer, Wine & Spirits",
    "ready-meals": "Prepared & Ready-to-Eat",
    "international": "International Foods",
    "other": "Other / Miscellaneous",
}


def validate_categories(supermarket_name: str, category_map: dict):
    """
    Ensures all mapped categories exist in STANDARD_CATEGORIES.
    Raises error if invalid category is found.
    """
    invalid = []
    for slug, mapped in category_map.items():
        if mapped not in STANDARD_CATEGORIES.values():
            invalid.append((slug, mapped))

    if invalid:
        raise ValueError(
            f"[{supermarket_name}] Invalid category mappings found: {invalid}\n"
            f"Valid categories are: {list(STANDARD_CATEGORIES.values())}"
        )
    else:
        print(f"[{supermarket_name}] Category mappings are valid.")

