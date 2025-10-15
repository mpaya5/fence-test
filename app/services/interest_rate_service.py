"""
Service for managing interest rate operations.
"""
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timezone

from ..schemas.endpoints.assets import AssetRequest
from ..smart_contracts.smart_contract_storage import SmartContractStorage


class InterestRateService:
    """Service for managing interest rate operations."""
    
    def __init__(self, smart_contract_storage: SmartContractStorage):
        self.storage = smart_contract_storage
    
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