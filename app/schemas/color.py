from sqlmodel import SQLModel

class ColorRead(SQLModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True