"""Authentication API endpoints."""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.models.user import User, get_user_by_username
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response Schemas

class LoginRequest(BaseModel):
    """Login request schema."""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, max_length=100, description="Password")


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserResponse(BaseModel):
    """User information response."""
    id: str
    username: str
    created_at: str

    class Config:
        from_attributes = True


# Endpoints

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return JWT token.

    Args:
        login_data: Login credentials (username, password)

    Returns:
        TokenResponse containing JWT access token and expiration time

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Retrieve user by username
    user = await get_user_by_username(login_data.username)

    # Verify user exists and password matches
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.username, "username": user.username}
    )

    # Calculate expiration time in seconds
    expires_in = settings.jwt_expires_minutes * 60

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.

    Args:
        current_user: Injected authenticated user from dependency

    Returns:
        User information (id, username, created_at)
    """
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        created_at=current_user.created_at.isoformat()
    )


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_token_endpoint(current_user: User = Depends(get_current_user)):
    """
    Verify if the provided token is valid.

    Args:
        current_user: Injected authenticated user from dependency

    Returns:
        Confirmation message with user info
    """
    return {
        "valid": True,
        "username": current_user.username
    }
