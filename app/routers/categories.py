from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from app.models.category import Category
from app.schemas.category import CategoryRead
from app.database import get_session

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories
