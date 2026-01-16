"""Storage service for file operations with local filesystem support."""

import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional
import aiofiles
from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    """Handle file storage operations with support for local filesystem."""

    def __init__(self):
        self.base_path = Path(settings.storage_path)
        self.uploads_path = self.base_path / "uploads"
        self.thumbnails_path = self.base_path / "thumbnails"

    async def save_file(
        self,
        file: UploadFile,
        collection_code: str,
        file_type: str = "photo"
    ) -> tuple[str, str]:
        """
        Save uploaded file to storage.

        Args:
            file: The uploaded file
            collection_code: Collection code for organizing files
            file_type: Type of file (photo or thumbnail)

        Returns:
            Tuple of (file_path, filename)
        """
        # Sanitize filename
        original_filename = self._sanitize_filename(file.filename or "unknown")

        # Generate unique filename
        file_uuid = uuid.uuid4().hex[:12]
        filename = f"{file_uuid}_{original_filename}"

        # Create directory structure: storage/uploads/{code}/{year}/{month}/
        now = datetime.now()
        year_month_path = Path(collection_code) / str(now.year) / f"{now.month:02d}"

        if file_type == "thumbnail":
            full_dir = self.thumbnails_path / year_month_path
        else:
            full_dir = self.uploads_path / year_month_path

        full_dir.mkdir(parents=True, exist_ok=True)

        # Full file path
        file_path = full_dir / filename

        # Reset file pointer before reading
        await file.seek(0)

        # Save file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        # Return relative path for database storage
        relative_path = str(file_path.relative_to(self.base_path))
        return relative_path, filename

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage.

        Args:
            file_path: Relative path to file

        Returns:
            True if deleted successfully
        """
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False

    def get_file_url(self, file_path: str) -> str:
        """
        Get URL for accessing file.

        Args:
            file_path: Relative path to file

        Returns:
            URL string for file access
        """
        # For local storage, return path relative to storage root
        # In production, this would return CDN/S3 URL
        return f"/storage/{file_path}"

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to prevent path traversal and invalid characters.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove path components
        filename = os.path.basename(filename)

        # Replace unsafe characters
        unsafe_chars = ['/', '\\', '..', '\0']
        for char in unsafe_chars:
            filename = filename.replace(char, '_')

        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:190] + ext

        return filename


# Global storage service instance
storage_service = StorageService()
