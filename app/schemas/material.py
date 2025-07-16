from sqlmodel import SQLModel

class MaterialRead(SQLModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True