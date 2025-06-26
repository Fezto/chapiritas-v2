from typing import Optional
from sqlmodel import Field

from app.models.base import BaseModel


class ColorProduct(BaseModel, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    color_id: Optional[int] = Field(default=None, foreign_key="color.id", primary_key=True)
