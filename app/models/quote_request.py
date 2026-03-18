from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    company_name = Column(String(150), nullable=True)
    message = Column(Text, nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    status = Column(String(50), nullable=False, default="new")

    created_at = Column(DateTime, nullable=False, server_default=func.now())
