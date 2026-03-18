from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.sql import func

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String(50), nullable=False, default="pending")
    total_amount = Column(Numeric(10, 2), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
