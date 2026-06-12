from datetime import UTC, datetime
from decimal import Decimal

from app.schemas.endpoints.assets import AssetRequest
from app.storage.base import InterestRateStorage


class InterestRateService:
    """Service for managing interest rate operations."""

    def __init__(self, storage: InterestRateStorage):
        self.storage = storage

    async def calculate_and_save_average_rate(self, assets: list[AssetRequest]) -> Decimal:
        if not assets:
            raise ValueError("Asset list cannot be empty")

        total_rate = sum(asset.interest_rate for asset in assets)
        average_rate = total_rate / len(assets)
        current_time = datetime.now(UTC).isoformat()

        await self.storage.save_interest_rate(average_rate, current_time)
        return average_rate

    async def get_current_rate(self) -> tuple[Decimal, str] | None:
        return await self.storage.get_current_interest_rate()
