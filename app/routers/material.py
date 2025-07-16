from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.material import Material
from app.schemas.material import MaterialRead
from app.database import get_session
from typing import List

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_model=List[MaterialRead], summary="Get all materials")
def get_all_brands(session: Session = Depends(get_session)):
    return session.exec(select(Material)).all()