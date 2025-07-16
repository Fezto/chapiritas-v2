from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.brand import Brand
from app.schemas.brand import BrandRead
from app.database import get_session
from typing import List

router = APIRouter(prefix="/brands", tags=["brands"])

@router.get("/", response_model=List[BrandRead], summary="Get all brands")
def get_all_brands(session: Session = Depends(get_session)):
    return session.exec(select(Brand)).all()
