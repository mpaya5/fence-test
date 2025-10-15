from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan of the FastAPI application.
    """
    try:
        logger.info("Starting FastAPI application...")
        yield
    except Exception as e:
        logger.error(f"Error starting FastAPI application: {e}")
        raise e
    finally:
        logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title="Fence Test",
    version="1.0.0",
    description="Fence Test",
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

# Include the API routes (exact paths as per README.md)
from app.api.v1.router import api_router

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fence Test!"}