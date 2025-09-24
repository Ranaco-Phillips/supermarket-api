from database.db_setup import Base, engine
from database import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!!")
