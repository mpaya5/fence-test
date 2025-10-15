from abc import ABC, abstractmethod
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timezone

from ..schemas.endpoints.assets import AssetRequest


class InterestRateStorage(ABC):
    """Abstract storage interface for interest rate data."""
    
    @abstractmethod
    async def save_interest_rate(self, rate: Decimal, timestamp: str) -> None:
        """Save an interest rate with timestamp."""
        pass
    
    @abstractmethod
    async def get_current_interest_rate(self) -> Optional[tuple[Decimal, str]]:
        """Get the current interest rate and timestamp."""
        pass


class InterestRateService:
    """Service for managing interest rate operations."""
    
    def __init__(self, storage: InterestRateStorage):
        self.storage = storage
    
    async def calculate_and_save_average_rate(self, assets: List[AssetRequest]) -> Decimal:
        """
        Calculate average interest rate from assets and save it.
        
        Args:
            assets: List of assets with their interest rates
            
        Returns:
            Decimal: The calculated average interest rate
            
        Raises:
            ValueError: If assets list is empty or invalid
        """
        if not assets:
            raise ValueError("Asset list cannot be empty")
        
        # Calculate average interest rate
        total_rate = sum(asset.interest_rate for asset in assets)
        average_rate = total_rate / len(assets)
        
        # Get current timestamp
        current_time = datetime.now(timezone.utc).isoformat()
        
        # Save to storage
        await self.storage.save_interest_rate(average_rate, current_time)
        
        return average_rate
    
    async def get_current_rate(self) -> Optional[tuple[Decimal, str]]:
        """
        Get the current stored interest rate.
        
        Returns:
            Optional[tuple[Decimal, str]]: Rate and timestamp, or None if not found
        """
        return await self.storage.get_current_interest_rate()