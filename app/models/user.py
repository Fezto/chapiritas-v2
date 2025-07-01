from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship

from .base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    last_name: str
    second_last_name: str
    email: str = Field(index=True, unique=True)
    email_verified_at: Optional[datetime] = None
    phone_number: Optional[str] = Field(default=None, unique=True)
    password: str
    two_factor_secret: Optional[str] = None
    two_factor_recovery_codes: Optional[str] = None
    two_factor_confirmed_at: Optional[datetime] = None
    url: Optional[str] = Field(default="default.png")
    remember_token: Optional[str] = None
    address_id: int = Field(default=1)
    gender_id: Optional[int] = Field(default=None, foreign_key="genders.id")
