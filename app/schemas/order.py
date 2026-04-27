from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    product_id: UUID
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    quote_id: UUID
    status: str
    total_amount: Decimal
    payment_status: str
    created_at: str | None = None
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}
