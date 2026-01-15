"""API dependencies for authentication and request processing."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.core.security import verify_token
from app.models.user import User, get_user_by_username

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer credentials containing the JWT token

    Returns:
        User document if authentication successful

    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Decode and verify token
        payload = verify_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retrieve user from database
    user = await get_user_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[User]:
    """
    Optional authentication dependency - returns user if token provided,
    None otherwise. Doesn't raise exception for missing token.

    Args:
        credentials: HTTP Bearer credentials (optional)

    Returns:
        User document if valid token provided, None otherwise
    """
    if credentials is None:
        return None

    token = credentials.credentials

    try:
        payload = verify_token(token)
        username: str = payload.get("sub")

        if username is None:
            return None

    except JWTError:
        return None

    user = await get_user_by_username(username)
    return user
