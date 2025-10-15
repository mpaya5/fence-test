from app.services.interest_rate_service import InterestRateService
from app.smart_contracts.smart_contract_storage import SmartContractStorage
from app.smart_contracts.client.web3_client import Web3Client
from app.core.config import settings


def get_interest_rate_service() -> InterestRateService:
    """Get the interest rate service instance with Smart Contract storage."""
    web3_client = Web3Client(
        rpc_url=settings.BLOCKCHAIN_RPC_URL,
        private_key=settings.HARDHAT_PRIVATE_KEY
    )
    storage = SmartContractStorage(web3_client)
    return InterestRateService(storage)
