from sqlmodel import SQLModel

class GenderRead(SQLModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True