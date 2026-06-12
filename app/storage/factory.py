from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import StorageBackend, settings
from app.database_handler.session import SessionLocal
from app.smart_contracts.client.web3_client import Web3Client
from app.smart_contracts.smart_contract_storage import SmartContractStorage
from app.storage.base import InterestRateStorage
from app.storage.postgres_storage import PostgresStorage


def get_db_if_postgres() -> Generator[Session | None]:
    if settings.STORAGE_BACKEND != StorageBackend.POSTGRES:
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_storage(db: Session | None = None) -> InterestRateStorage:
    if settings.STORAGE_BACKEND == StorageBackend.SMART_CONTRACT:
        return SmartContractStorage(Web3Client())

    if db is None:
        raise RuntimeError("Database session is required for postgres storage backend")

    return PostgresStorage(db)


def get_storage(db: Session | None = Depends(get_db_if_postgres)) -> InterestRateStorage:
    return create_storage(db)
