from sqlmodel import Field

from app.models.base import BaseModel


class ProductSize(BaseModel, table=True):
    __tablename__ = 'product_size'
    
    # Foreign keys
    size_id: int = Field(foreign_key="sizes.id")
    product_id: int = Field(foreign_key="products.id")