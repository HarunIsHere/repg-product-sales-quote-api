from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.user import User
from app.schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/from-quote/{quote_id}",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def create_order_from_quote(quote_id, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found",
        )

    if quote.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved quotes can be converted to orders",
        )

    existing_order = db.query(Order).filter(Order.quote_id == quote.id).first()

    if existing_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An order already exists for this quote",
        )

    quote_items = db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).all()

    if not quote_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create order from quote without items",
        )

    order = Order(
        user_id=quote.user_id,
        quote_id=quote.id,
        status="created",
        total_amount=quote.total_amount,
        payment_status="pending",
    )

    db.add(order)
    db.flush()

    for quote_item in quote_items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=quote_item.product_id,
                quantity=quote_item.quantity,
                unit_price=quote_item.unit_price,
            )
        )

    quote.status = "converted"

    db.commit()
    db.refresh(order)

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        quote_id=order.quote_id,
        status=order.status,
        total_amount=order.total_amount,
        payment_status=order.payment_status,
        created_at=str(order.created_at) if order.created_at else None,
        items=order_items,
    )


@router.get("/my", response_model=list[OrderResponse])
def get_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []

    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        result.append(
            OrderResponse(
                id=order.id,
                user_id=order.user_id,
                quote_id=order.quote_id,
                status=order.status,
                total_amount=order.total_amount,
                payment_status=order.payment_status,
                created_at=str(order.created_at) if order.created_at else None,
                items=order_items,
            )
        )

    return result


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if (
        current_user.role not in {"admin", "super_admin"}
        and order.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        quote_id=order.quote_id,
        status=order.status,
        total_amount=order.total_amount,
        payment_status=order.payment_status,
        created_at=str(order.created_at) if order.created_at else None,
        items=order_items,
    )
