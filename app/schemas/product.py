from typing import Optional, List

from sqlmodel import SQLModel, Field

from app.schemas.image import ImageRead
from app.schemas.brand import BrandRead
from app.schemas.category import CategoryRead
from app.schemas.color import ColorRead
from app.schemas.gender import GenderRead
from app.schemas.material import MaterialRead
from app.schemas.size import SizeRead


class ProductBase(SQLModel):
    name: str
    price: float
    quantity: Optional[int]
    user_id: int
    brand_id: int
    category_id: int
    description: Optional[str]

class ProductCreate(ProductBase):
    color_id: Optional[int]
    gender_id: Optional[int]
    material_id: Optional[int]
    size_id: Optional[int]

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    description: Optional[str] = None

class ProductRead(SQLModel):
    id: int
    name: str
    price: float
    quantity: Optional[int]
    user_id: int
    description: Optional[str]

    brand: Optional[BrandRead]
    category: Optional[CategoryRead]
    images: List[ImageRead] = []

    colors: List[ColorRead] = []
    genders: List[GenderRead] = []
    materials: List[MaterialRead] = []
    sizes: List[SizeRead] = []


class ProductFilter(SQLModel):
    categories: Optional[List[int]] = None
    genders: Optional[List[int]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    order_by: Optional[int] = Field(0, description="1=name, 2=price, 3=price desc")