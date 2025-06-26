from typing import Optional, List

from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    price: float
    quantity: Optional[int]
    user_id: int
    brand_id: int
    category_id: int
    description: Optional[str]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    description: Optional[str] = None

class ProductRead(ProductBase):
    id: int
    images: List["ImageRead"] = []


class ProductFilter(SQLModel):
    categories: Optional[List[int]] = None
    genders: Optional[List[int]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    order_by: Optional[int] = Field(0, description="1=name, 2=price, 3=price desc")