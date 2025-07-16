from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.color import Color
from app.schemas.color import ColorRead
from app.database import get_session
from typing import List

router = APIRouter(prefix="/colors", tags=["colors"])

@router.get("/", response_model=List[ColorRead], summary="Get all colors")
def get_all_brands(session: Session = Depends(get_session)):
    return session.exec(select(Color)).all()