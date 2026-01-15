#Just to verify the database connection
from app.db import engine
from sqlmodel import Session

def test_connection():
    try:
        with Session(engine) as session:
            print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Database connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()