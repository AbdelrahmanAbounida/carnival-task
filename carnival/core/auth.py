from fastapi.security import APIKeyHeader
from carnival.core.config import settings
from fastapi import Depends, HTTPException, status, Request


api_key_header = APIKeyHeader(name="server-api-key", auto_error=False)
keys = [settings.SERVER_API_KEY]


def get_static_api_key(request: Request, api_key: str = Depends(api_key_header)) -> str:
    # TODO:: move to generic decorator for public routes
    current_path = request.url.path
    print(f"current_path: {current_path}")
    if current_path == "/":
        return True

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing API Key",
        )

    if api_key in keys:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )
