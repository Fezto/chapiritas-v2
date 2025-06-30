from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class MaterialProduct(BaseModel, table=True):
    __tablename__ = 'material_product'
    product_id: Optional[int] = Field(
        default=None, foreign_key="products.id", primary_key=True
    )
    material_id: Optional[int] = Field(
        default=None, foreign_key="materials.id", primary_key=True
    )
