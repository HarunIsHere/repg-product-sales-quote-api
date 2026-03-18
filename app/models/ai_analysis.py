from sqlalchemy import Column, Float, ForeignKey, Integer, JSON, String, Text

from app.db.base import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True, index=True)

    quote_request_id = Column(Integer, ForeignKey("quote_requests.id"), nullable=False, unique=True)

    detected_sector = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)

    recommended_products = Column(JSON, nullable=True)

    notes = Column(Text, nullable=True)
