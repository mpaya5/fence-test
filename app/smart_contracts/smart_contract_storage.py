import time
from typing import Optional
from decimal import Decimal
from .client.web3_client import Web3Client
from app.core.logger import logger

class SmartContractStorage:
    """Smart Contract storage for interest rate data."""
    
    def __init__(self, web3_client: Web3Client):
        """
        Initialize Smart Contract Storage.
        
        Args:
            web3_client: Configured Web3Client instance
        """
        self.web3_client = web3_client
    
    async def save_interest_rate(self, rate: Decimal, timestamp: str) -> None:
        """
        Save interest rate to smart contract.
        
        Args:
            rate: Interest rate as Decimal
            timestamp: ISO format timestamp string
            
        Raises:
            Exception: If transaction fails or cannot be confirmed
        """
        try:
            # Convert ISO timestamp to Unix timestamp
            import datetime
            dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            unix_timestamp = int(dt.timestamp())
            
            # Update interest rate in smart contract and wait for confirmation
            tx_hash, receipt = self.web3_client.update_interest_rate(rate, unix_timestamp, wait_for_confirmation=True)
            
            # Verify transaction was successful
            if not tx_hash:
                raise Exception("Transaction failed - no transaction hash returned")
            
            if receipt is None:
                raise Exception("Transaction confirmation failed - no receipt received")
            
            # Check if transaction was successful
            if receipt.get('status') == 0:
                raise Exception(f"Transaction failed with status 0. TX: {tx_hash}")
            
            # Log successful transaction details
            gas_used = receipt.get('gasUsed', 'unknown')
            block_number = receipt.get('blockNumber', 'unknown')
            logger.info(f"✅ Interest rate updated successfully!")
            logger.info(f"   📝 TX Hash: {tx_hash}")
            logger.info(f"   ⛽ Gas Used: {gas_used}")
            logger.info(f"   📦 Block: {block_number}")
                
        except Exception as e:
            # Log error and re-raise with more context
            error_msg = f"Failed to save interest rate to smart contract: {str(e)}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg) from e
    
    async def get_current_interest_rate(self) -> Optional[tuple[Decimal, str]]:
        """
        Get current interest rate from smart contract.
        
        Returns:
            Tuple of (rate, timestamp) or None if no data
        """
        result = self.web3_client.get_interest_rate()
        
        if result is None:
            return None
        
        rate, unix_timestamp = result
        
        # Convert Unix timestamp back to ISO format
        import datetime
        dt = datetime.datetime.fromtimestamp(unix_timestamp, tz=datetime.timezone.utc)
        iso_timestamp = dt.isoformat()
        
        return rate, iso_timestamp
