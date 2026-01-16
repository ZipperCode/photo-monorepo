"""Photo model for uploaded photo management.

This module defines the Photo document model and Pydantic schemas
for creating and managing uploaded photos.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class Photo(Document):
    """
    Photo document model for MongoDB.

    Represents an uploaded photo with metadata, file paths, and processing status.
    """

    # Collection reference (indexed for fast lookups)
    collection_code: Indexed(str)

    # File information
    filename: str
    file_path: str
    thumbnail_path: Optional[str] = None
    file_size: int  # in bytes
    mime_type: str

    # Image dimensions
    dimensions: Dict[str, int] = Field(default_factory=dict)  # {width, height}

    # Upload information
    uploaded_at: Indexed(datetime) = Field(default_factory=datetime.now)
    uploader_info: Dict[str, Optional[str]] = Field(default_factory=dict)  # {ip_address, user_agent}

    # EXIF metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)  # {camera_make, camera_model, exif_data}

    # Processing status
    processing_status: str = "pending"  # pending, processed, failed

    # Soft delete
    is_deleted: bool = False

    class Settings:
        name = "photos"
        indexes = [
            "collection_code",
            "uploaded_at",
        ]


class PhotoCreate(BaseModel):
    """Schema for creating a new photo."""

    collection_code: str
    filename: str
    file_path: str
    thumbnail_path: Optional[str] = None
    file_size: int
    mime_type: str
    dimensions: Dict[str, int] = Field(default_factory=dict)
    uploader_info: Dict[str, Optional[str]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PhotoResponse(BaseModel):
    """Schema for photo response."""

    id: str
    collection_code: str
    filename: str
    file_path: str
    thumbnail_path: Optional[str]
    file_size: int
    mime_type: str
    dimensions: Dict[str, int]
    uploaded_at: datetime
    uploader_info: Dict[str, Optional[str]]
    metadata: Dict[str, Any]
    processing_status: str

    class Config:
        from_attributes = True
