import os

import pytest

from app.storage.factory import create_storage
from app.storage.postgres_storage import PostgresStorage


def test_create_storage_uses_postgres_by_default(db_session):
    os.environ["STORAGE_BACKEND"] = "postgres"
    storage = create_storage(db_session)
    assert isinstance(storage, PostgresStorage)


def test_create_storage_requires_db_for_postgres():
    os.environ["STORAGE_BACKEND"] = "postgres"
    with pytest.raises(RuntimeError, match="Database session is required"):
        create_storage(None)


def test_create_storage_smart_contract(monkeypatch):
    os.environ["STORAGE_BACKEND"] = "smart_contract"
    from app.core import config as config_module

    updated_settings = config_module.Settings()
    monkeypatch.setattr("app.storage.factory.settings", updated_settings)

    sentinel = object()
    monkeypatch.setattr("app.storage.factory.Web3Client", lambda: object())
    monkeypatch.setattr("app.storage.factory.SmartContractStorage", lambda _client: sentinel)

    assert create_storage(None) is sentinel
