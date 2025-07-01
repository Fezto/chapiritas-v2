# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field
from sqlmodel import SQLModel

class UserBase(SQLModel):
    name: str
    last_name: str
    second_last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    # si necesitas forzar address_id aquí, puedes añadir:
    address_id: int = Field(default=1)

class UserRead(UserBase):
    id: int
    email_verified_at: Optional[datetime] = None
    url: Optional[str] = None
    remember_token: Optional[str] = None
    address_id: int
    gender_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
