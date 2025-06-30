from typing import Optional
from pydantic import BaseModel

class ImageBase(BaseModel):
    url: str
    description: Optional[str] = None
    order: Optional[int] = 1

class ImageCreate(ImageBase):
    product_id: int

class ImageRead(ImageBase):
    id: int
    product_id: int

class ImageUpdate(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None