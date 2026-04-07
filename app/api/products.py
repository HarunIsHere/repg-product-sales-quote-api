from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    stock_status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if stock_status:
        query = query.filter(Product.stock_status == stock_status)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.post(
    "/",
    response_model=ProductResponse,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="SKU already exists",
        )

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = product_update.model_dump(exclude_unset=True)

    if "sku" in update_data:
        existing_product = (
            db.query(Product)
            .filter(Product.sku == update_data["sku"], Product.id != product_id)
            .first()
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SKU already exists",
            )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
