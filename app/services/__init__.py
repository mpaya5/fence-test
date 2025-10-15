from app.services.interest_rate_service import InterestRateService, InterestRateStorage


def get_interest_rate_service() -> InterestRateService:
    """Get the interest rate service instance."""
    storage = InterestRateStorage()
    return InterestRateService(storage)
