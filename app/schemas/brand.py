from sqlmodel import SQLModel
from typing import Optional

class BrandRead(SQLModel):
    id: Optional[int] = None
    name: str
