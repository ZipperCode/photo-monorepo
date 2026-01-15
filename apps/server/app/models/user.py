"""User model for administrator authentication."""

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field

from app.core.security import hash_password, verify_password


class User(Document):
    """
    User document model for MongoDB.

    Represents an administrator user with authentication credentials.
    """
    username: Indexed(str, unique=True)  # Unique indexed username
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # MongoDB collection name
        indexes = [
            "username",  # Index for fast username lookups
        ]

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return verify_password(password, self.hashed_password)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(BaseModel):
    """Schema for user responses (excludes password)."""
    id: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


# Database operations

async def get_user_by_username(username: str) -> Optional[User]:
    """
    Retrieve a user by username.

    Args:
        username: Username to search for

    Returns:
        User document if found, None otherwise
    """
    return await User.find_one(User.username == username)


async def create_user(username: str, password: str) -> User:
    """
    Create a new user with hashed password.

    Args:
        username: Username for the new user
        password: Plain text password (will be hashed)

    Returns:
        Created User document

    Raises:
        ValueError: If username already exists
    """
    # Check if user already exists
    existing_user = await get_user_by_username(username)
    if existing_user:
        raise ValueError(f"Username '{username}' already exists")

    # Create user with hashed password
    user = User(
        username=username,
        hashed_password=hash_password(password)
    )

    await user.insert()
    return user
