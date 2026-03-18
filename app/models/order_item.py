from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    spare_part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=True)

    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=True)

    order = relationship("Order", backref="order_items")
    product = relationship("Product")
    spare_part = relationship("SparePart")
