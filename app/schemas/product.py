from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    currency: str
    sku: str
    category: str
    subcategory: str
    product_type: str
    stock_status: str
    lead_time: str
    technical_specs: dict
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    product_type: Optional[str] = None
    stock_status: Optional[str] = None
    lead_time: Optional[str] = None
    technical_specs: Optional[dict] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: UUID

    model_config = {"from_attributes": True}
