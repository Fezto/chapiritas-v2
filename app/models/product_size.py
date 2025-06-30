from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class ProductSize(BaseModel, table=True):
    __tablename__ = 'product_size'
    product_id: Optional[int] = Field(default=None, foreign_key="products.id", primary_key=True)
    size_id: Optional[int] = Field(default=None, foreign_key="sizes.id", primary_key=True)