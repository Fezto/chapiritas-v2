from typing import Optional

from sqlmodel import SQLModel


class ImageRead(SQLModel):
    id: int
    url: str
    description: Optional[str]
    order: int