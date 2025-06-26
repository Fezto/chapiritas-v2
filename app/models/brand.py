from typing import List

from sqlmodel import Relationship

from app.models.base import BaseModel


class Brand(BaseModel, table=True):
    __tablename__ = 'brand'
    name: str
    products: List["Product"] = Relationship(back_populates="brand")