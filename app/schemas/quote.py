from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class QuoteItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)


class QuoteCreate(BaseModel):
    items: list[QuoteItemCreate] = Field(..., min_length=1)


class QuoteItemResponse(BaseModel):
    id: int
    product_id: UUID
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class QuoteResponse(BaseModel):
    id: UUID
    user_id: int
    status: str
    total_amount: Decimal
    created_at: str | None = None
    items: list[QuoteItemResponse] = []

    model_config = {"from_attributes": True}
