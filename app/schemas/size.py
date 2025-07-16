from sqlmodel import SQLModel

class SizeRead(SQLModel):
    id: int
    name: str
    
    class Config: 
        orm_mode = True