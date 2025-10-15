from app.services.interest_rate_service import InterestRateService
from app.repositories.interest_rate_repository import InterestRateRepository
from app.database_handler.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


def get_interest_rate_service(db: Session = Depends(get_db)) -> InterestRateService:
    """Get the interest rate service instance with database repository."""
    repository = InterestRateRepository(db)
    return InterestRateService(repository)
