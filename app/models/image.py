from typing import Optional

from sqlmodel import Field, Relationship
from app.models.base import BaseModelSimple


class Image(BaseModelSimple, table=True):
    __tablename__ = 'images'

    product_id: int = Field(foreign_key="products.id")
    url: str
    description: Optional[str] = None
    order: Optional[int] = Field(default=1)

    product: "Product" = Relationship(back_populates="images")
