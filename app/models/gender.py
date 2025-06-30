from typing import List

from sqlmodel import Relationship

from app.models.base import BaseModel
from app.models.gender_product import GenderProduct


class Gender(BaseModel, table=True):
    __tablename__ = 'genders'
    name: str
    products: List["Product"] = Relationship(
        back_populates="genders", link_model=GenderProduct
    )
