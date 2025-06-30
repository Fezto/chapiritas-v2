from typing import List

from sqlmodel import Relationship

from app.models.base import BaseModel


class Category(BaseModel, table=True):
    __tablename__ = 'categories'
    name: str
    products: List["Product"] = Relationship(back_populates="category")