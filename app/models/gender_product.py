from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class GenderProduct(BaseModel, table=True):
    __tablename__ = 'gender_product'

    product_id: Optional[int] = Field(
        default=None, foreign_key="products.id", primary_key=True
    )
    gender_id: Optional[int] = Field(
        default=None, foreign_key="genders.id", primary_key=True
    )