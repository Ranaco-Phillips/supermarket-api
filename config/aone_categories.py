# config/aone_categories.py
from config.categories import STANDARD_CATEGORIES, validate_categories

AONE_BASE_URL = "https://aonesupermarkets.com/collections/"

AONE_CATEGORIES = {
    "cakes-bread": "Bakery & Bread",
    "rice-pasta-peas": "Pantry Staples & Dry Goods",
    "alcoholic-drinks": "Beer, Wine & Spirits",
    "teas-soft-drinks": "Beverages",
    "frozen": "Frozen Foods",
    "sugar-home-baking": "Bakery & Bread",
    "tins-cans-packets": "Pantry Staples & Dry Goods",
    "breakfast-cereal": "Breakfast & Cereal",
    "biscuits-crackers": "Snacks & Confectionery",
    "jam-honey-spreads": "Snacks & Confectionery",
    "condiments-marinades": "Condiments, Sauces & Spices",
    "jarred-goods": "Pantry Staples & Dry Goods",
    "desserts": "Frozen Foods",
    "cooking-sauces-meal-kits": "Condiments, Sauces & Spices",
   
}


# Validate before scraping
validate_categories("AOne", AONE_CATEGORIES)