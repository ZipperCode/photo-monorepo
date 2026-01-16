"""Photo service for orchestrating photo upload workflow."""

import magic
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException
import logging

from app.models.photo import Photo, PhotoCreate
from app.models.collection import Collection
from app.services.storage_service import storage_service
from app.services.image_service import image_service

logger = logging.getLogger(__name__)


class PhotoService:
    """Orchestrate photo upload workflow with validation and processing."""

    # Allowed MIME types
    ALLOWED_MIME_TYPES = {
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/heic',
        'image/heif'
    }

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif'}

    async def upload_photo(
        self,
        file: UploadFile,
        collection_code: str,
        uploader_info: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a single photo with validation and processing.

        Args:
            file: Uploaded file
            collection_code: Collection code
            uploader_info: Optional uploader information (ip, user_agent)

        Returns:
            Dictionary with upload result
        """
        try:
            # Validate collection
            collection = await Collection.find_one(Collection.code == collection_code.upper())
            if not collection:
                return {
                    'success': False,
                    'filename': file.filename,
                    'error': 'Collection not found'
                }

            if collection.status != 'active':
                return {
                    'success': False,
                    'filename': file.filename,
                    'error': f'Collection is {collection.status}'
                }

            # Validate file
            validation_error = await self._validate_file(file, collection)
            if validation_error:
                return {
                    'success': False,
                    'filename': file.filename,
                    'error': validation_error
                }

            # Reset file pointer after validation
            await file.seek(0)

            # Save original file
            file_path, filename = await storage_service.save_file(
                file,
                collection_code.upper(),
                'photo'
            )

            # Get full path for processing
            full_path = Path(storage_service.base_path) / file_path

            # Get file size
            file_size = full_path.stat().st_size

            # Get MIME type
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(str(full_path))

            # Get dimensions
            dimensions = image_service.get_dimensions(str(full_path))
            dimensions_dict = {'width': dimensions[0], 'height': dimensions[1]} if dimensions else {}

            # Extract EXIF metadata
            metadata = image_service.extract_exif(str(full_path))

            # Generate thumbnail
            thumbnail_path = None
            # Calculate thumbnail path using Path operations
            relative_file_path = Path(file_path)
            thumbnail_relative = Path('thumbnails') / relative_file_path.relative_to('uploads')
            thumbnail_full_path = storage_service.base_path / thumbnail_relative

            if image_service.generate_thumbnail(str(full_path), str(thumbnail_full_path)):
                thumbnail_path = str(thumbnail_relative)

            # Create photo record
            photo_data = PhotoCreate(
                collection_code=collection_code.upper(),
                filename=filename,
                file_path=file_path,
                thumbnail_path=thumbnail_path,
                file_size=file_size,
                mime_type=mime_type,
                dimensions=dimensions_dict,
                uploader_info=uploader_info or {},
                metadata=metadata
            )

            photo = Photo(**photo_data.model_dump())
            photo.processing_status = 'processed'
            await photo.insert()

            # Update collection statistics
            await self._update_collection_stats(collection, file_size)

            return {
                'success': True,
                'filename': file.filename,
                'photo_id': str(photo.id),
                'file_size': file_size
            }

        except Exception as e:
            logger.error(f"Failed to upload photo {file.filename}: {e}")
            return {
                'success': False,
                'filename': file.filename,
                'error': str(e)
            }

    async def _validate_file(
        self,
        file: UploadFile,
        collection: Collection
    ) -> Optional[str]:
        """
        Validate uploaded file.

        Args:
            file: Uploaded file
            collection: Collection document

        Returns:
            Error message if validation fails, None otherwise
        """
        # Check file extension
        if file.filename:
            ext = Path(file.filename).suffix.lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                return f'File type {ext} not allowed'

        # Read first chunk for magic number validation
        content = await file.read(2048)
        await file.seek(0)  # Reset file pointer

        # Validate MIME type by magic number
        mime = magic.Magic(mime=True)
        detected_mime = mime.from_buffer(content)

        if detected_mime not in self.ALLOWED_MIME_TYPES:
            return f'Invalid file type: {detected_mime}'

        # Check file size limit
        max_size = collection.settings.get('max_file_size_mb', 50) * 1024 * 1024
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset

        if file_size > max_size:
            return f'File size exceeds limit of {max_size / 1024 / 1024}MB'

        return None

    async def _update_collection_stats(
        self,
        collection: Collection,
        file_size: int
    ) -> None:
        """
        Update collection statistics after upload.

        Args:
            collection: Collection document
            file_size: Size of uploaded file in bytes
        """
        from datetime import datetime

        collection.statistics['photo_count'] += 1
        collection.statistics['total_size_bytes'] += file_size
        collection.statistics['last_upload_at'] = datetime.now()

        await collection.save()


# Global photo service instance
photo_service = PhotoService()
