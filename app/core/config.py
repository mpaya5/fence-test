from enum import Enum

from decouple import config
from pydantic_settings import BaseSettings


class StorageBackend(str, Enum):
    POSTGRES = "postgres"
    SMART_CONTRACT = "smart_contract"


def _parse_storage_backend(value: str) -> StorageBackend:
    return StorageBackend(value.lower())


class Settings(BaseSettings):
    API_KEY_NAME: str = config("API_KEY_NAME", default="api_key", cast=str)
    API_KEY_AUTH: str = config("API_KEY_AUTH", default="your-secret-api-key-here", cast=str)

    STORAGE_BACKEND: StorageBackend = config(
        "STORAGE_BACKEND",
        default=StorageBackend.POSTGRES.value,
        cast=_parse_storage_backend,
    )

    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="postgres", cast=str)
    POSTGRES_USER: str = config("POSTGRES_USER", default="fence_user", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="fence_password", cast=str)
    POSTGRES_DB: str = config("POSTGRES_DB", default="fence_test", cast=str)
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432", cast=str)

    BLOCKCHAIN_RPC_URL: str = config(
        "BLOCKCHAIN_RPC_URL", default="http://localhost:8545", cast=str
    )
    HARDHAT_PRIVATE_KEY: str = config(
        "HARDHAT_PRIVATE_KEY",
        default="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
        cast=str,
    )
    GAS_LIMIT: int = config("GAS_LIMIT", default=100000, cast=int)

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
