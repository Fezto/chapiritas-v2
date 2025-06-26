from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class MaterialProduct(BaseModel, table=True):
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    material_id: Optional[int] = Field(
        default=None, foreign_key="material.id", primary_key=True
    )
