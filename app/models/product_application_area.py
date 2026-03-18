from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProductApplicationArea(Base):
    __tablename__ = "product_application_areas"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    application_area_id = Column(Integer, ForeignKey("application_areas.id"), nullable=False)

    product = relationship("Product", backref="product_application_areas")
    application_area = relationship("ApplicationArea", backref="product_application_areas")
