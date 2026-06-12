import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("API_KEY_AUTH", "test-api-key")
os.environ.setdefault("STORAGE_BACKEND", "postgres")

from app.database_handler.models.base import Base
from app.main import app
from app.storage.factory import get_db_if_postgres

TEST_DATABASE_URL = "sqlite://"


@pytest.fixture
def db_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db_if_postgres():
        yield db_session

    app.dependency_overrides[get_db_if_postgres] = override_get_db_if_postgres
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def api_headers():
    return {"api_key": "test-api-key"}
