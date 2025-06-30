from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select, or_

from app.models import Product
from app.schemas.product import (
    ProductRead, ProductCreate, ProductUpdate, ProductFilter
)
from app.session import get_session

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/filter", response_model=List[ProductRead], summary="Filter products")
def filter_products(
    session: Session = Depends(get_session),
    categories: Optional[List[int]] = Query(None),
    genders: Optional[List[int]] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    order_by: Optional[int] = Query(0)
):
    query = select(Product)
    if categories:
        query = query.where(Product.category_id.in_(categories))
    if genders:
        query = query.join(Product.genders).where(
            or_(*[Product.genders.any(id=g) for g in genders])
        )
    if min_price is not None and max_price is not None:
        query = query.where(Product.price.between(min_price, max_price))
    if order_by == 1:
        query = query.order_by(Product.name)
    elif order_by == 2:
        query = query.order_by(Product.price)
    elif order_by == 3:
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.id)
    return session.exec(query).all()

# LIST
@router.get("/", response_model=List[ProductRead], summary="List products")
def list_products(
    session: Session = Depends(get_session),
    category: Optional[int] = Query(None)
):
    query = select(Product)
    if category:
        query = query.where(Product.category_id == category)
    return session.exec(query).all()

# GET
@router.get("/{product_id}", response_model=ProductRead, summary="Get product by ID")
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# CREATE
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Create product")
def create_product(
    product_in: ProductCreate,
    session: Session = Depends(get_session)
):
    product = Product(**product_in.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# UPDATE
@router.patch("/{product_id}", response_model=ProductRead, summary="Update product")
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product_in.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# DELETE
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete product")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()

# FILTER

