from decouple import config
import os


class Settings:
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="", cast=str)
    POSTGRES_USER: str = config("POSTGRES_USER", default="", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="", cast=str)
    POSTGRES_DB: str = config("POSTGRES_DB", default="", cast=str)
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432", cast=str)

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
