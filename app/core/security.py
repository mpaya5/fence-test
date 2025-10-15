from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.core.config import settings


API_KEY_NAME = settings.API_KEY_NAME
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    """
    Validate API key from request header

    Args:
        api_key_header: API key from request header

    Returns:
        str: Validated API key

    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key_header:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="No API key provided"
        )

    if api_key_header != settings.EXPLORER_BACKEND_API_KEY_AUTH:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")

    return api_key_header
