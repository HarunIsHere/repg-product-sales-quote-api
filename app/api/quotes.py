from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.product import Product
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.user import User
from app.schemas.quote import QuoteCreate, QuoteResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/", response_model=QuoteResponse)
def create_quote(
    quote_data: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not quote_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quote must contain at least one item",
        )

    total_amount = Decimal("0.00")
    db_items: list[QuoteItem] = []

    for item in quote_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: {item.product_id}",
            )

        unit_price = Decimal(str(product.price))
        total_amount += unit_price * item.quantity

        db_items.append(
            QuoteItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price,
            )
        )

    db_quote = Quote(
        user_id=current_user.id,
        status="pending",
        total_amount=total_amount,
    )

    db.add(db_quote)
    db.flush()

    for db_item in db_items:
        db_item.quote_id = db_quote.id
        db.add(db_item)

    db.commit()
    db.refresh(db_quote)

    items = db.query(QuoteItem).filter(QuoteItem.quote_id == db_quote.id).all()

    return QuoteResponse(
        id=db_quote.id,
        user_id=db_quote.user_id,
        status=db_quote.status,
        total_amount=db_quote.total_amount,
        created_at=str(db_quote.created_at) if db_quote.created_at else None,
        items=items,
    )


@router.get("/my", response_model=list[QuoteResponse])
def get_my_quotes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quotes = db.query(Quote).filter(Quote.user_id == current_user.id).all()
    result = []

    for quote in quotes:
        items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()
        result.append(
            QuoteResponse(
                id=quote.id,
                user_id=quote.user_id,
                status=quote.status,
                total_amount=quote.total_amount,
                created_at=str(quote.created_at) if quote.created_at else None,
                items=items,
            )
        )

    return result


@router.get("/{quote_id}", response_model=QuoteResponse)
def get_quote(
    quote_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found",
        )

    if current_user.role not in {"admin", "super_admin"} and quote.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

    return QuoteResponse(
        id=quote.id,
        user_id=quote.user_id,
        status=quote.status,
        total_amount=quote.total_amount,
        created_at=str(quote.created_at) if quote.created_at else None,
        items=items,
    )


@router.patch(
    "/{quote_id}/status",
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def update_quote_status(
    quote_id: UUID,
    status_value: str = Query(...),
    db: Session = Depends(get_db),
):
    allowed_statuses = {"pending", "approved", "rejected", "converted"}

    if status_value not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status",
        )

    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found",
        )

    quote.status = status_value
    db.commit()
    db.refresh(quote)

    return {
        "message": "Quote status updated successfully",
        "quote_id": str(quote.id),
        "status": quote.status,
    }
