from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    part_number = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    product = relationship("Product", backref="spare_parts")
