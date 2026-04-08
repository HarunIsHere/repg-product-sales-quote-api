from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    user_id: int
    quote_id: UUID
    status: str
    total_amount: Decimal
    payment_status: str
    created_at: str | None = None

    model_config = {"from_attributes": True}
