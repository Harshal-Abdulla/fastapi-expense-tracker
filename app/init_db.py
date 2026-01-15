# table creation script needs to be run manually
#python -m app.init_db
#Why? you dont want table cration code to run every time FastAPI starts

from sqlmodel import SQLModel
from app.db import engine
from typing import Optional

# IMPORTANT: import models so they register on SQLModel.metadata
# this import has side-effects: it defines the table classes
from app import models  # ensures User and Expense are loaded

def init():
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init()
