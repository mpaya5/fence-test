from abc import ABC, abstractmethod
from decimal import Decimal


class InterestRateStorage(ABC):
    """Storage abstraction for persisting and reading interest rates."""

    @abstractmethod
    async def save_interest_rate(self, rate: Decimal, timestamp: str) -> None:
        """Persist an interest rate with an ISO-8601 timestamp."""

    @abstractmethod
    async def get_current_interest_rate(self) -> tuple[Decimal, str] | None:
        """Return the latest rate and ISO-8601 timestamp, or None if unset."""
