"""Collection model for photo collection management.

This module defines the Collection document model and Pydantic schemas
for creating, updating, and responding with collection data.
"""

from datetime import datetime
from typing import Optional, List

from beanie import Document, Indexed
from pydantic import BaseModel, Field, validator


class Collection(Document):
    """
    Collection document model for MongoDB.

    Represents a photo collection with a unique access code, settings,
    and statistics tracking.
    """

    # Unique 6-character access code (indexed for fast lookups)
    code: Indexed(str, unique=True)

    # Basic information
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    # Collection status
    status: str = Field(default="active")  # active, archived, closed

    # Upload settings
    settings: dict = Field(
        default_factory=lambda: {
            "allow_upload": True,
            "max_file_size": 10 * 1024 * 1024,  # 10MB in bytes
            "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        }
    )

    # Usage statistics
    statistics: dict = Field(
        default_factory=lambda: {
            "total_photos": 0,
            "total_size_bytes": 0,
            "last_upload_at": None
        }
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str  # Username of creator
    is_deleted: bool = False  # Soft delete flag

    class Settings:
        """Beanie ODM settings."""
        name = "collections"
        indexes = [
            "code",  # Unique index already set via Indexed()
            "created_at",
            "status",
            "is_deleted",
        ]

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "code": "ABC123",
                "name": "Wedding Photos",
                "description": "John & Jane's Wedding",
                "status": "active",
                "settings": {
                    "allow_upload": True,
                    "max_file_size": 10485760,
                    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"]
                },
                "statistics": {
                    "total_photos": 0,
                    "total_size_bytes": 0,
                    "last_upload_at": None
                },
                "created_at": "2024-01-15T10:30:00",
                "created_by": "admin",
                "is_deleted": False
            }
        }


# Pydantic Schemas for API

class CollectionCreate(BaseModel):
    """Schema for creating a new collection."""
    name: str = Field(..., min_length=3, max_length=100, description="Collection name")
    description: Optional[str] = Field(None, max_length=500, description="Collection description")
    status: str = Field(default="active", description="Collection status")
    settings: Optional[dict] = Field(None, description="Upload settings")

    @validator('status')
    def validate_status(cls, v):
        """Validate status is one of the allowed values."""
        allowed = {"active", "archived", "closed"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v


class CollectionUpdate(BaseModel):
    """Schema for updating an existing collection."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None
    settings: Optional[dict] = None

    @validator('status')
    def validate_status(cls, v):
        """Validate status is one of the allowed values."""
        if v is not None:
            allowed = {"active", "archived", "closed"}
            if v not in allowed:
                raise ValueError(f"Status must be one of {allowed}")
        return v


class CollectionResponse(BaseModel):
    """Schema for collection API responses."""
    id: str
    code: str
    name: str
    description: Optional[str]
    status: str
    settings: dict
    statistics: dict
    created_at: datetime
    created_by: str

    class Config:
        """Enable population from ORM objects."""
        from_attributes = True


class ValidateCodeRequest(BaseModel):
    """Schema for code validation request."""
    code: str = Field(..., min_length=6, max_length=6, description="6-character collection code")


class ValidateCodeResponse(BaseModel):
    """Schema for code validation response."""
    valid: bool
    collection: Optional[dict] = None
    message: Optional[str] = None


# Database Operations

async def get_collection_by_code(code: str) -> Optional[Collection]:
    """
    Retrieve a collection by its code.

    Args:
        code: Collection code (case-insensitive)

    Returns:
        Collection document if found and not deleted, None otherwise

    Example:
        >>> collection = await get_collection_by_code("ABC123")
        >>> if collection:
        ...     print(collection.name)
    """
    # Normalize code to uppercase for case-insensitive lookup
    normalized_code = code.strip().upper()

    return await Collection.find_one(
        Collection.code == normalized_code,
        Collection.is_deleted == False
    )


async def get_collection_by_id(collection_id: str) -> Optional[Collection]:
    """
    Retrieve a collection by its MongoDB ID.

    Args:
        collection_id: MongoDB ObjectId as string

    Returns:
        Collection document if found and not deleted, None otherwise
    """
    return await Collection.find_one(
        Collection.id == collection_id,
        Collection.is_deleted == False
    )


async def create_collection(
    data: CollectionCreate,
    created_by: str
) -> Collection:
    """
    Create a new collection with auto-generated unique code.

    Args:
        data: Collection creation data
        created_by: Username of the creator

    Returns:
        Created Collection document

    Raises:
        ValueError: If unable to generate unique code
        RuntimeError: If code generation fails after max retries

    Example:
        >>> data = CollectionCreate(name="Wedding Photos", description="John & Jane")
        >>> collection = await create_collection(data, created_by="admin")
        >>> print(collection.code)  # e.g., "ABC123"
    """
    from app.utils.code_generator import generate_unique_code

    # Generate unique code
    code = await generate_unique_code(
        check_fn=lambda c: get_collection_by_code(c) is not None,
        max_retries=10
    )

    # Merge user settings with defaults
    default_settings = {
        "allow_upload": True,
        "max_file_size": 10 * 1024 * 1024,
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    }

    final_settings = default_settings.copy()
    if data.settings:
        final_settings.update(data.settings)

    # Create collection
    collection = Collection(
        code=code,
        name=data.name,
        description=data.description,
        status=data.status,
        settings=final_settings,
        created_by=created_by
    )

    await collection.insert()
    return collection


async def list_collections(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None
) -> List[Collection]:
    """
    List collections with pagination and optional status filter.

    Args:
        skip: Number of documents to skip (for pagination)
        limit: Maximum number of documents to return
        status_filter: Optional status filter (active/archived/closed)

    Returns:
        List of Collection documents

    Example:
        >>> # Get first 20 collections
        >>> collections = await list_collections(skip=0, limit=20)
        >>> # Get only active collections
        >>> active = await list_collections(status_filter="active")
    """
    query = Collection.find(Collection.is_deleted == False)

    # Apply status filter if provided
    if status_filter:
        query = query.find(Collection.status == status_filter)

    # Sort by creation date (newest first) and apply pagination
    return await query.sort("-created_at").skip(skip).limit(limit).to_list()


async def update_collection(
    code: str,
    data: CollectionUpdate
) -> Optional[Collection]:
    """
    Update an existing collection.

    Args:
        code: Collection code
        data: Update data (only provided fields will be updated)

    Returns:
        Updated Collection document, or None if not found

    Example:
        >>> update = CollectionUpdate(name="Updated Name", status="archived")
        >>> collection = await update_collection("ABC123", update)
    """
    collection = await get_collection_by_code(code)

    if not collection:
        return None

    # Update only provided fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(collection, field, value)

    await collection.save()
    return collection


async def delete_collection(code: str) -> bool:
    """
    Soft delete a collection by marking it as deleted.

    Args:
        code: Collection code

    Returns:
        True if collection was deleted, False if not found

    Example:
        >>> success = await delete_collection("ABC123")
        >>> if success:
        ...     print("Collection deleted")
    """
    collection = await get_collection_by_code(code)

    if not collection:
        return False

    # Soft delete: mark as deleted instead of removing
    collection.is_deleted = True
    await collection.save()
    return True


async def update_statistics(
    code: str,
    photo_size: int
) -> Optional[Collection]:
    """
    Update collection statistics after a photo upload.

    Args:
        code: Collection code
        photo_size: Size of uploaded photo in bytes

    Returns:
        Updated Collection document, or None if not found

    Example:
        >>> collection = await update_statistics("ABC123", photo_size=1024000)
    """
    collection = await get_collection_by_code(code)

    if not collection:
        return None

    collection.statistics["total_photos"] += 1
    collection.statistics["total_size_bytes"] += photo_size
    collection.statistics["last_upload_at"] = datetime.utcnow()

    await collection.save()
    return collection


async def count_collections(status_filter: Optional[str] = None) -> int:
    """
    Count total collections, optionally filtered by status.

    Args:
        status_filter: Optional status filter

    Returns:
        Count of collections

    Example:
        >>> total = await count_collections()
        >>> active_count = await count_collections(status_filter="active")
    """
    query = Collection.find(Collection.is_deleted == False)

    if status_filter:
        query = query.find(Collection.status == status_filter)

    return await query.count()
