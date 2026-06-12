from fastapi import Depends

from app.services.interest_rate_service import InterestRateService
from app.storage.base import InterestRateStorage
from app.storage.factory import get_storage


def get_interest_rate_service(
    storage: InterestRateStorage = Depends(get_storage),
) -> InterestRateService:
    return InterestRateService(storage)
