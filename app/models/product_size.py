from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class ProductSize(BaseModel, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    size_id: Optional[int] = Field(default=None, foreign_key="size.id", primary_key=True)