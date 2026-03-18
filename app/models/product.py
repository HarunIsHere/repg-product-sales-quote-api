from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    short_description = Column(String(300), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    min_operating_temperature_c = Column(Numeric(6, 2), nullable=True)
    max_operating_temperature_c = Column(Numeric(6, 2), nullable=True)
    daily_water_output_liters = Column(Numeric(10, 2), nullable=True)
    min_power_output_kwh = Column(Numeric(10, 2), nullable=True)
    max_power_output_kwh = Column(Numeric(10, 2), nullable=True)
    portable = Column(Boolean, nullable=False, default=False)
    off_grid_capable = Column(Boolean, nullable=False, default=False)
    catalog_url = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
