
from typing import Optional, List
from sqlmodel import Field, Relationship

from app.models.base import BaseModel
from app.models.brand import Brand
from app.models.category import Category
from app.models.color_product import ColorProduct
from app.models.gender_product import GenderProduct
from app.models.image import Image
from app.models.material_product import MaterialProduct
from app.models.product_size import ProductSize

class Product(BaseModel, table=True):
    __tablename__ = 'products'

    name: str
    price: float
    quantity: Optional[int]
    user_id: int = Field(foreign_key="users.id")
    brand_id: int = Field(foreign_key="brands.id")
    category_id: int = Field(foreign_key="categories.id")
    description: Optional[str]

    brand: Brand = Relationship(back_populates="products")
    category: Category = Relationship(back_populates="products")
    images: List[Image] = Relationship(back_populates="product", cascade_delete=True, passive_deletes=True)  # <- Ya no en string
    colors: List["Color"] = Relationship(back_populates="products", link_model=ColorProduct)
    genders: List["Gender"] = Relationship(back_populates="products", link_model=GenderProduct)
    materials: List["Material"] = Relationship(back_populates="products", link_model=MaterialProduct)
    sizes: List["Size"] = Relationship(back_populates="products", link_model=ProductSize)
