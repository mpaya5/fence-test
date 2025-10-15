from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    API_KEY_NAME: str = config("API_KEY_NAME", default="api_key", cast=str)
    API_KEY_AUTH: str = config("API_KEY_AUTH", default="your-secret-api-key-here", cast=str)

    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="postgres", cast=str)
    POSTGRES_USER: str = config("POSTGRES_USER", default="fence_user", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="fence_password", cast=str)
    POSTGRES_DB: str = config("POSTGRES_DB", default="fence_test", cast=str)
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432", cast=str)

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()