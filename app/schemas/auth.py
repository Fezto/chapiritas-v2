# app/schemas/auth.py
from pydantic import EmailStr, Field
from sqlmodel import SQLModel
from typing import Optional

class RegisterRequest(SQLModel):
    name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    second_last_name: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone_number: Optional[str] = None
    # si quieres que el cliente decida otra dirección:
    # address_id: Optional[int] = None

class LoginRequest(SQLModel):
    email: EmailStr
    password: str

class TokenResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(SQLModel):
    email: EmailStr

class ResetPasswordRequest(SQLModel):
    email: EmailStr
    token: str
    password: str
