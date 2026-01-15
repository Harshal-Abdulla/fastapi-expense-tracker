# Our API endpoints
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from passlib.hash import pbkdf2_sha256
from typing import List, Optional
from pydantic import BaseModel
from .db import engine
from .models import User, Expense, UserCreate, UserRead, ExpenseUpdate, ExpenseCreate

router = APIRouter()

# Input / output schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    # Pydantic v2: allow building model from ORM/SQLModel objects
    model_config = {"from_attributes": True}

class ExpenseCreate(BaseModel):
    user_id: int
    category: str
    amount: float
    currency : Optional[str] = "EUR"
    note: Optional[str] = None

class LoginIn(BaseModel):
    email: str
    password: str

# User endpoints
@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == payload.email)).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        try:
            password_hash = pbkdf2_sha256.hash(payload.password)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Password invalid or too long")
        user = User(name=payload.name, email=payload.email, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

#List all users
@router.get("/users", response_model=List[UserRead])
def list_users():
    with Session(engine) as session:
        result = session.exec(select(User))
        users = result.all()
        return users
    
# list user with user id
@router.get("/user/{user_id}")
def ger_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code = 404, detail = "User not found")
        return user


# Expense endpoints
@router.post("/expenses")
def create_expense(expense_in: ExpenseCreate):
        with Session(engine) as session:
            expense = Expense(
                user_id = expense_in.user_id,
                category = expense_in.category,
                amount = expense_in.amount, 
                currency = expense_in.currency,
                note = expense_in.note
            )
            session.add(expense)
            session.commit()
            session.refresh(expense)
            return expense

@router.get("/expenses")
def list_expenses(user_id : Optional[int] = None):
    with Session(engine) as session:
        return session.exec(select(Expense)).all()
    
@router.post("/login")
def login(payload: LoginIn):
        # 1. open a DB session
    with Session(engine) as session:
        # 2. find the user by email
        user = session.exec(select(User).where(User.email == payload.email)).first()
        if not user:        # 3. if user not found -> return failure
            return {"success":False, "message":"Invalid credentials"}
        # 4. verify the plaintext password against stored hash
        ok = pbkdf2_sha256.verify(payload.password, user.password_hash)
        if not ok:
            return{"success":False, "message":"Invalid credentials"}
        
        return {"success":True, "user_id":user.id, "message":"Login successful"}

@router.get("/expenses/{expense_id}")
def get_expense(expense_id : int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id=id)
        if not expense:
            raise HTTPException(status_code = 404, detail="Expense Not found")
    return expense


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        session.delete(expense)
        session.commit()

        return {"message": "Expense deleted successfully"}

@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, payload: ExpenseUpdate):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        if payload.category is not None:
            expense.category = payload.category
        if payload.currency is not None:
            expense.currency = payload.currency
        if payload.note is not None:
            expense.note = payload.note
        if payload.amount is not None:
            expense.amount = payload.amount
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense