from typing import List

from sqlmodel import Relationship

from app.models.base import BaseModel
from app.models.material_product import MaterialProduct


class Material(BaseModel, table=True):
    __tablename__ = 'material'
    name: str
    products: List["Product"] = Relationship(
        back_populates="materials", link_model=MaterialProduct
    )