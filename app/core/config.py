from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    API_KEY_NAME: str = config("API_KEY_NAME", default="api_key", cast=str)
    API_KEY_AUTH: str = config("API_KEY_AUTH", default="", cast=str)

settings = Settings()