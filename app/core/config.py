from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    # API Configuration
    API_KEY_NAME: str = config("API_KEY_NAME", default="api_key", cast=str)
    API_KEY_AUTH: str = config("API_KEY_AUTH", default="your-secret-api-key-here", cast=str)
    
    # Blockchain Configuration
    BLOCKCHAIN_RPC_URL: str = config("BLOCKCHAIN_RPC_URL", default="http://localhost:8545", cast=str)
    HARDHAT_PRIVATE_KEY: str = config("HARDHAT_PRIVATE_KEY", default="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80", cast=str)
    GAS_LIMIT: int = config("GAS_LIMIT", default=100000, cast=int)
    GAS_PRICE_GWEI: int = config("GAS_PRICE_GWEI", default=20, cast=int)

settings = Settings()