from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base


class ApplicationArea(Base):
    __tablename__ = "application_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
