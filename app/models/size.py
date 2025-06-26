from typing import List

from sqlmodel import Relationship

from app.models.base import BaseModel
from app.models.product_size import ProductSize


class Size(BaseModel, table=True):
    __tablename__ = 'size'
    name: str
    products: List["Product"] = Relationship(
        back_populates="sizes", link_model=ProductSize
    )