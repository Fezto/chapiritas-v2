from sqlmodel import Field

from app.models.base import BaseModel


class MaterialProduct(BaseModel, table=True):
    __tablename__ = 'material_product'
    
    # Foreign keys
    material_id: int = Field(foreign_key="materials.id")
    product_id: int = Field(foreign_key="products.id")
