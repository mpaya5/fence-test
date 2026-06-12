from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.interest_rate_repository import InterestRateRepository
from app.storage.base import InterestRateStorage


class PostgresStorage(InterestRateStorage):
    """PostgreSQL-backed storage using the repository pattern."""

    def __init__(self, db: Session):
        self._repository = InterestRateRepository(db)

    async def save_interest_rate(self, rate: Decimal, timestamp: str) -> None:
        updated_at = datetime.fromisoformat(timestamp)
        self._repository.save_interest_rate(rate, updated_at)

    async def get_current_interest_rate(self) -> tuple[Decimal, str] | None:
        return self._repository.get_current_interest_rate()
