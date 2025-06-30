from typing import Optional
from sqlmodel import Field

from app.models.base import BaseModel


class ColorProduct(BaseModel, table=True):
    __tablename__ = 'color_product'
    product_id: Optional[int] = Field(default=None, foreign_key="products.id", primary_key=True)
    color_id: Optional[int] = Field(default=None, foreign_key="colors.id", primary_key=True)
