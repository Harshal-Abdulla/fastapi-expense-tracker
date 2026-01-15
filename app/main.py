#FAST API app started; entry point of our API
#uvicorn app.main:app --reload : runs this file
from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routes import router   

app = FastAPI(title="Expense Tracker - FastAPI")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running, Boss!"}

# INCLUDE ROUTES
app.include_router(router)