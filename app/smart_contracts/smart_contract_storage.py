import datetime
from decimal import Decimal

from app.core.logger import logger
from app.smart_contracts.client.web3_client import Web3Client
from app.storage.base import InterestRateStorage


class SmartContractStorage(InterestRateStorage):
    """Smart Contract storage for interest rate data."""

    def __init__(self, web3_client: Web3Client):
        self.web3_client = web3_client

    async def save_interest_rate(self, rate: Decimal, timestamp: str) -> None:
        try:
            dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            unix_timestamp = int(dt.timestamp())

            tx_hash, receipt = self.web3_client.update_interest_rate(
                rate, unix_timestamp, wait_for_confirmation=True
            )

            if not tx_hash:
                raise RuntimeError("Transaction failed - no transaction hash returned")

            if receipt is None:
                raise RuntimeError("Transaction confirmation failed - no receipt received")

            if receipt.get("status") == 0:
                raise RuntimeError(f"Transaction failed with status 0. TX: {tx_hash}")

            gas_used = receipt.get("gasUsed", "unknown")
            block_number = receipt.get("blockNumber", "unknown")
            logger.info("Interest rate updated on-chain")
            logger.info("TX Hash: %s", tx_hash)
            logger.info("Gas Used: %s", gas_used)
            logger.info("Block: %s", block_number)

        except Exception as e:
            error_msg = f"Failed to save interest rate to smart contract: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    async def get_current_interest_rate(self) -> tuple[Decimal, str] | None:
        result = self.web3_client.get_interest_rate()

        if result is None:
            return None

        rate, unix_timestamp = result
        dt = datetime.datetime.fromtimestamp(unix_timestamp, tz=datetime.UTC)
        return rate, dt.isoformat()
