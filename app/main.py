from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting FastAPI application...")
        logger.info(f"Storage backend: {settings.STORAGE_BACKEND.value}")
        yield
    except Exception as e:
        logger.error(f"Error starting FastAPI application: {e}")
        raise
    finally:
        logger.info("Shutting down FastAPI application...")


app = FastAPI(
    title="Fence Test API",
    version="1.0.0",
    description=(
        "Asset interest rate management API. "
        "Technical assessment rebuilt as a portfolio-quality FastAPI backend."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Fence Test!",
        "storage_backend": settings.STORAGE_BACKEND.value,
    }
