import asyncio
from decimal import Decimal

from app.schemas.endpoints.assets import AssetRequest
from app.services.interest_rate_service import InterestRateService
from app.storage.postgres_storage import PostgresStorage


def test_calculate_and_save_average_rate(db_session):
    storage = PostgresStorage(db_session)
    service = InterestRateService(storage)
    assets = [
        AssetRequest(id="a", interest_rate=Decimal("100")),
        AssetRequest(id="b", interest_rate=Decimal("50")),
    ]

    asyncio.run(service.calculate_and_save_average_rate(assets))
    result = asyncio.run(service.get_current_rate())

    assert result is not None
    rate, _ = result
    assert rate == Decimal("75")


def test_get_current_rate_returns_none_when_empty(db_session):
    storage = PostgresStorage(db_session)
    service = InterestRateService(storage)
    assert asyncio.run(service.get_current_rate()) is None
