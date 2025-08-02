from sqlmodel import Field

from app.models.base import BaseModel


class GenderProduct(BaseModel, table=True):
    __tablename__ = 'gender_product'
    
    # Foreign keys
    gender_id: int = Field(foreign_key="genders.id")
    product_id: int = Field(foreign_key="products.id")