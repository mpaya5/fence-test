"""
Schemas for asset-related endpoints.
"""
from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal


class AssetRequest(BaseModel):
    """Request schema for a single asset."""
    id: str = Field(..., description="Unique identifier for the asset")
    interest_rate: Decimal = Field(..., ge=0, description="Interest rate for the asset")
    
    class Config:
        json_encoders = {
            Decimal: str
        }


class AssetListRequest(BaseModel):
    """Request schema for asset list endpoint."""
    assets: List[AssetRequest] = Field(..., min_items=1, description="List of assets to process")
    
    class Config:
        json_encoders = {
            Decimal: str
        }


class InterestRateResponse(BaseModel):
    """Response schema for interest rate endpoints."""
    interest_rate: Decimal = Field(..., description="Current average interest rate")
    updated_at: str = Field(..., description="Timestamp when the rate was last updated")
    
    class Config:
        json_encoders = {
            Decimal: str
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Additional error details")
