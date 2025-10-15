from fastapi import APIRouter
from app.api.v1.endpoints import assets

api_router = APIRouter()

# Include asset endpoints (exact paths as per README.md)
api_router.include_router(
    assets.router,
    tags=["assets"]
)