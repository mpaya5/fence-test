from app.services.interest_rate_service import InterestRateService
from app.smart_contracts.smart_contract_storage import SmartContractStorage
from app.smart_contracts.client.web3_client import Web3Client


def get_interest_rate_service() -> InterestRateService:
    """Get the interest rate service instance with Smart Contract storage."""
    # Web3Client is now a singleton - no need to pass parameters
    web3_client = Web3Client()
    storage = SmartContractStorage(web3_client)
    return InterestRateService(storage)
