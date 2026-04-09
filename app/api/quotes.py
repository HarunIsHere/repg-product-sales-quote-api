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
    payload: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quote must contain at least one item",
        )

    total_amount = 0
    validated_items = []

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: {item.product_id}",
            )

        unit_price = product.price
        total_amount += unit_price * item.quantity

        validated_items.append(
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": unit_price,
            }
        )

    quote = Quote(
        user_id=current_user.id,
        status="pending",
        total_amount=total_amount,
    )

    db.add(quote)
    db.flush()

    for item in validated_items:
        db.add(
            QuoteItem(
                quote_id=quote.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            )
        )

    db.commit()
    db.refresh(quote)

    quote_items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

    return QuoteResponse(
        id=quote.id,
        user_id=quote.user_id,
        status=quote.status,
        total_amount=quote.total_amount,
        created_at=str(quote.created_at) if quote.created_at else None,
        items=quote_items,
    )


@router.get(
    "/",
    response_model=list[QuoteResponse],
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def get_all_quotes(
    status_value: str | None = Query(default=None),
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Quote)

    if status_value:
        query = query.filter(Quote.status == status_value)

    if user_id is not None:
        query = query.filter(Quote.user_id == user_id)

    quotes = query.order_by(Quote.created_at.desc()).all()
    result = []

    for quote in quotes:
        quote_items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

        result.append(
            QuoteResponse(
                id=quote.id,
                user_id=quote.user_id,
                status=quote.status,
                total_amount=quote.total_amount,
                created_at=str(quote.created_at) if quote.created_at else None,
                items=quote_items,
            )
        )

    return result


@router.get("/my", response_model=list[QuoteResponse])
def get_my_quotes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quotes = db.query(Quote).filter(Quote.user_id == current_user.id).all()
    result = []

    for quote in quotes:
        quote_items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

        result.append(
            QuoteResponse(
                id=quote.id,
                user_id=quote.user_id,
                status=quote.status,
                total_amount=quote.total_amount,
                created_at=str(quote.created_at) if quote.created_at else None,
                items=quote_items,
            )
        )

    return result


@router.get("/{quote_id}", response_model=QuoteResponse)
def get_quote(
    quote_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found",
        )

    if (
        current_user.role not in {"admin", "super_admin"}
        and quote.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    quote_items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

    return QuoteResponse(
        id=quote.id,
        user_id=quote.user_id,
        status=quote.status,
        total_amount=quote.total_amount,
        created_at=str(quote.created_at) if quote.created_at else None,
        items=quote_items,
    )


@router.patch(
    "/{quote_id}/status",
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def update_quote_status(
    quote_id,
    status_value: str,
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

    return {"message": f"Quote status updated to {status_value}"}
