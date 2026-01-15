#Contains all SQLModel classes and Pydantic models
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

#db models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)   

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    category: Optional[str] = None
    amount: float
    currency: Optional[str] = "EUR"
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Input / output schemas
class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str

    # Pydantic v2: allow building model from ORM/SQLModel objects
    model_config = {"from_attributes": True}

class ExpenseCreate(SQLModel):
    user_id: int
    category: Optional[str] = None
    amount: float
    currency: Optional[str] = "EUR"
    note: Optional[str] = None

class LoginIn(BaseModel):
    email: str
    password: str

class ExpenseRead(SQLModel):
    id: int
    user_id: int
    category: Optional[str] = None
    amount: float
    currency: Optional[str] = "EUR"
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExpenseUpdate(SQLModel):
    category: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = "EUR"
    note: Optional[str] = None