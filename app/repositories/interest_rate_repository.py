from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Optional
from datetime import datetime
from app.database_handler.models.interest_rate import InterestRate as InterestRateModel


class InterestRateRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_interest_rate(self, rate: Decimal, timestamp: datetime) -> None:
        """Save interest rate to database."""
        interest_rate = InterestRateModel(rate=rate, updated_at=timestamp)
        self.db.add(interest_rate)
        self.db.commit()
        self.db.refresh(interest_rate)

    def get_current_interest_rate(self) -> Optional[tuple[Decimal, str]]:
        """Get the most recent interest rate."""
        latest = self.db.query(InterestRateModel).order_by(InterestRateModel.updated_at.desc()).first()
        if latest:
            return (latest.rate, latest.updated_at.isoformat())
        return None