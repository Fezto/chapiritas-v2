from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class GenderProduct(BaseModel, table=True):
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    gender_id: Optional[int] = Field(
        default=None, foreign_key="gender.id", primary_key=True
    )