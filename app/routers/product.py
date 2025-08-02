from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select, or_

from app.models import Product
from app.models.color_product import ColorProduct
from app.models.gender_product import GenderProduct
from app.models.material_product import MaterialProduct
from app.models.product_size import ProductSize
from app.models.brand import Brand
from app.models.category import Category
from app.models.color import Color
from app.models.gender import Gender
from app.models.material import Material
from app.models.size import Size
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
    """
    Crear un producto con relaciones many-to-many.
    Implementa transacciones, validaciones y manejo de errores.
    """
    try:
        # 1. Validar que las entidades relacionadas existan
        _validate_related_entities(session, product_in)
        
        # 2. Crear el producto base (sin las relaciones many-to-many)
        product_data = product_in.dict(exclude={'color_ids', 'gender_ids', 'material_ids', 'size_ids'})
        product = Product(**product_data)
        
        session.add(product)
        session.flush()  # Obtener el ID sin hacer commit
        
        # 3. Crear las relaciones many-to-many
        _create_product_relations(session, product.id, product_in)
        
        # 4. Commit único al final
        session.commit()
        session.refresh(product)
        
        return product
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


def _validate_related_entities(session: Session, product_in: ProductCreate):
    """Validar que todas las entidades relacionadas existan"""
    
    # Validar marca
    brand = session.get(Brand, product_in.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail=f"Brand with id {product_in.brand_id} not found")
    
    # Validar categoría
    category = session.get(Category, product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {product_in.category_id} not found")
    
    # Validar colores
    if product_in.color_ids:
        colors = session.exec(select(Color).where(Color.id.in_(product_in.color_ids))).all()
        found_ids = {color.id for color in colors}
        missing_ids = set(product_in.color_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Colors not found: {missing_ids}")
    
    # Validar géneros
    if product_in.gender_ids:
        genders = session.exec(select(Gender).where(Gender.id.in_(product_in.gender_ids))).all()
        found_ids = {gender.id for gender in genders}
        missing_ids = set(product_in.gender_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Genders not found: {missing_ids}")
    
    # Validar materiales
    if product_in.material_ids:
        materials = session.exec(select(Material).where(Material.id.in_(product_in.material_ids))).all()
        found_ids = {material.id for material in materials}
        missing_ids = set(product_in.material_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Materials not found: {missing_ids}")
    
    # Validar tallas
    if product_in.size_ids:
        sizes = session.exec(select(Size).where(Size.id.in_(product_in.size_ids))).all()
        found_ids = {size.id for size in sizes}
        missing_ids = set(product_in.size_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Sizes not found: {missing_ids}")


def _create_product_relations(session: Session, product_id: int, product_in: ProductCreate):
    """Crear todas las relaciones many-to-many de forma eficiente"""
    
    # Crear relaciones de colores
    if product_in.color_ids:
        color_products = [
            ColorProduct(product_id=product_id, color_id=color_id)
            for color_id in product_in.color_ids
        ]
        session.add_all(color_products)
    
    # Crear relaciones de géneros
    if product_in.gender_ids:
        gender_products = [
            GenderProduct(product_id=product_id, gender_id=gender_id)
            for gender_id in product_in.gender_ids
        ]
        session.add_all(gender_products)
    
    # Crear relaciones de materiales
    if product_in.material_ids:
        material_products = [
            MaterialProduct(product_id=product_id, material_id=material_id)
            for material_id in product_in.material_ids
        ]
        session.add_all(material_products)
    
    # Crear relaciones de tallas
    if product_in.size_ids:
        product_sizes = [
            ProductSize(product_id=product_id, size_id=size_id)
            for size_id in product_in.size_ids
        ]
        session.add_all(product_sizes)


def _validate_update_related_entities(session: Session, product_in: ProductUpdate):
    """Validar que todas las entidades relacionadas existan para updates"""
    
    # Validar marca si se está actualizando
    if product_in.brand_id is not None:
        brand = session.get(Brand, product_in.brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail=f"Brand with id {product_in.brand_id} not found")
    
    # Validar categoría si se está actualizando
    if product_in.category_id is not None:
        category = session.get(Category, product_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail=f"Category with id {product_in.category_id} not found")
    
    # Validar colores si se proporcionaron
    if product_in.color_ids is not None:
        colors = session.exec(select(Color).where(Color.id.in_(product_in.color_ids))).all()
        found_ids = {color.id for color in colors}
        missing_ids = set(product_in.color_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Colors not found: {missing_ids}")
    
    # Validar géneros si se proporcionaron
    if product_in.gender_ids is not None:
        genders = session.exec(select(Gender).where(Gender.id.in_(product_in.gender_ids))).all()
        found_ids = {gender.id for gender in genders}
        missing_ids = set(product_in.gender_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Genders not found: {missing_ids}")
    
    # Validar materiales si se proporcionaron
    if product_in.material_ids is not None:
        materials = session.exec(select(Material).where(Material.id.in_(product_in.material_ids))).all()
        found_ids = {material.id for material in materials}
        missing_ids = set(product_in.material_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Materials not found: {missing_ids}")
    
    # Validar tallas si se proporcionaron
    if product_in.size_ids is not None:
        sizes = session.exec(select(Size).where(Size.id.in_(product_in.size_ids))).all()
        found_ids = {size.id for size in sizes}
        missing_ids = set(product_in.size_ids) - found_ids
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Sizes not found: {missing_ids}")


def _update_product_relations(session: Session, product_id: int, product_in: ProductUpdate):
    """Actualizar relaciones many-to-many reemplazando completamente las existentes"""
    
    # Actualizar colores si se proporcionaron
    if product_in.color_ids is not None:
        # Eliminar relaciones existentes
        session.exec(
            select(ColorProduct).where(ColorProduct.product_id == product_id)
        ).all()
        session.query(ColorProduct).filter(ColorProduct.product_id == product_id).delete()
        
        # Crear nuevas relaciones
        if product_in.color_ids:  # Solo si no está vacío
            color_products = [
                ColorProduct(product_id=product_id, color_id=color_id)
                for color_id in product_in.color_ids
            ]
            session.add_all(color_products)
    
    # Actualizar géneros si se proporcionaron
    if product_in.gender_ids is not None:
        session.query(GenderProduct).filter(GenderProduct.product_id == product_id).delete()
        if product_in.gender_ids:
            gender_products = [
                GenderProduct(product_id=product_id, gender_id=gender_id)
                for gender_id in product_in.gender_ids
            ]
            session.add_all(gender_products)
    
    # Actualizar materiales si se proporcionaron
    if product_in.material_ids is not None:
        session.query(MaterialProduct).filter(MaterialProduct.product_id == product_id).delete()
        if product_in.material_ids:
            material_products = [
                MaterialProduct(product_id=product_id, material_id=material_id)
                for material_id in product_in.material_ids
            ]
            session.add_all(material_products)
    
    # Actualizar tallas si se proporcionaron
    if product_in.size_ids is not None:
        session.query(ProductSize).filter(ProductSize.product_id == product_id).delete()
        if product_in.size_ids:
            product_sizes = [
                ProductSize(product_id=product_id, size_id=size_id)
                for size_id in product_in.size_ids
            ]
            session.add_all(product_sizes)


# UPDATE
@router.patch("/{product_id}", response_model=ProductRead, summary="Update product")
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualizar un producto y sus relaciones many-to-many.
    Implementa validaciones, transacciones y reemplaza completamente las relaciones.
    """
    try:
        # 1. Verificar que el producto existe
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 2. Validar entidades relacionadas si se están actualizando
        _validate_update_related_entities(session, product_in)
        
        # 3. Actualizar campos básicos del producto
        product_data = product_in.dict(
            exclude_unset=True,
            exclude={'color_ids', 'gender_ids', 'material_ids', 'size_ids'}
        )
        for key, value in product_data.items():
            setattr(product, key, value)
        
        # 4. Actualizar relaciones many-to-many si se proporcionaron
        _update_product_relations(session, product_id, product_in)
        
        # 5. Commit único al final
        session.add(product)
        session.commit()
        session.refresh(product)
        
        return product
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )

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

