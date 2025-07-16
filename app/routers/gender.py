from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.gender import Gender
from app.schemas.gender import GenderRead
from app.database import get_session
from typing import List

router = APIRouter(prefix="/genders", tags=["gender"])

@router.get("/", response_model=List[GenderRead], summary="Get all genders")
def get_all_brands(session: Session = Depends(get_session)):
    return session.exec(select(Gender)).all()