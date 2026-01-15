#Database connection file so the connection stays isolated and all other files can import this

import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env")

# Create SQLModel/SQLAlchemy engine connected to Postgres
engine = create_engine(DATABASE_URL, echo=True) # Echo prints the SQL statements for debugging to terminal

# Helper to create tables (used by app startup)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
