from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    # API Configuration
    API_KEY_NAME: str = config("API_KEY_NAME", default="api_key", cast=str)
    API_KEY_AUTH: str = config("API_KEY_AUTH", default="your-secret-api-key-here", cast=str)
    
    # Blockchain Configuration
    BLOCKCHAIN_RPC_URL: str = config("BLOCKCHAIN_RPC_URL", default="http://localhost:8545", cast=str)
    CONTRACT_ADDRESS: str = config("CONTRACT_ADDRESS", default="", cast=str)
    PRIVATE_KEY: str = config("PRIVATE_KEY", default="", cast=str)
    GAS_LIMIT: int = config("GAS_LIMIT", default=100000, cast=int)
    GAS_PRICE_GWEI: int = config("GAS_PRICE_GWEI", default=20, cast=int)

settings = Settings()