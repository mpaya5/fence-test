from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_api_key
from app.schemas.endpoints.assets import (
    AssetRequest,
    InterestRateResponse,
    ErrorResponse
)
from app.services import get_interest_rate_service, InterestRateService

router = APIRouter()


@router.post(
    "/asset",
    response_model=InterestRateResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Update Assets and Calculate Average Interest Rate",
    description="Receives a list of assets and updates the average interest rate"
)
async def update_assets(
    assets: list[AssetRequest],
    api_key: str = Depends(get_api_key),
    service: InterestRateService = Depends(get_interest_rate_service),
):
    """
    Update assets and calculate the average interest rate.
    
    Args:
        assets: List of assets with their interest rates (as per README.md example)
        api_key: API key for authentication
        
    Returns:
        InterestRateResponse: The calculated average interest rate
        
    Raises:
        HTTPException: If the request data is invalid or processing fails
    """
    try:
        # Calculate and save average interest rate
        average_rate = await service.calculate_and_save_average_rate(assets)
        
        # Get the stored data to return with timestamp
        result = await service.get_current_rate()
        _, timestamp = result
        
        return InterestRateResponse(
            interest_rate=average_rate,
            updated_at=timestamp
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/interest_rate",
    response_model=InterestRateResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Interest rate not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Current Interest Rate",
    description="Returns the current average interest rate stored in the system"
)
async def get_interest_rate(
    api_key: str = Depends(get_api_key),
    service: InterestRateService = Depends(get_interest_rate_service),
):
    """
    Get the current average interest rate.
    
    Args:
        api_key: API key for authentication
        
    Returns:
        InterestRateResponse: The current average interest rate
        
    Raises:
        HTTPException: If the interest rate cannot be retrieved
    """
    try:
        # Get current interest rate
        result = await service.get_current_rate()
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No interest rate found. Please update assets first."
            )
        
        rate, timestamp = result
        
        return InterestRateResponse(
            interest_rate=rate,
            updated_at=timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
