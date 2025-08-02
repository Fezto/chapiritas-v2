from sqlmodel import Field

from app.models.base import BaseModel


class ColorProduct(BaseModel, table=True):
    __tablename__ = 'color_product'
    
    # Foreign keys
    color_id: int = Field(foreign_key="colors.id")
    product_id: int = Field(foreign_key="products.id")
