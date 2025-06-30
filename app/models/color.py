from typing import List

from sqlmodel import Relationship

from app.models.color_product import ColorProduct
from app.models.base import BaseModel


class Color(BaseModel, table=True):
    __tablename__ = 'colors'
    name: str
    products: List["Product"] = Relationship(
        back_populates="colors", link_model=ColorProduct
    )