from sqlalchemy import Column, Integer, DateTime, Numeric
from datetime import datetime
from app.database_handler.models.base import Base


class InterestRate(Base):
    __tablename__ = "interest_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
