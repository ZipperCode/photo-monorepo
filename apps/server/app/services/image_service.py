"""Image processing service for thumbnails and EXIF extraction."""

from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ExifTags
import logging

logger = logging.getLogger(__name__)


class ImageService:
    """Handle image processing operations including thumbnails and EXIF."""

    def __init__(self):
        self.thumbnail_size = (400, 400)

    def generate_thumbnail(
        self,
        image_path: str,
        thumbnail_path: str
    ) -> bool:
        """
        Generate thumbnail for image maintaining aspect ratio.

        Args:
            image_path: Path to original image
            thumbnail_path: Path where thumbnail should be saved

        Returns:
            True if successful, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background

                # Generate thumbnail maintaining aspect ratio
                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)

                # Ensure directory exists
                Path(thumbnail_path).parent.mkdir(parents=True, exist_ok=True)

                # Save as JPEG
                img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)

            return True
        except Exception as e:
            logger.error(f"Failed to generate thumbnail: {e}")
            return False

    def extract_exif(self, image_path: str) -> Dict[str, Any]:
        """
        Extract EXIF metadata from image.

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with EXIF data
        """
        exif_data = {}

        try:
            with Image.open(image_path) as img:
                exif = img.getexif()

                if exif:
                    # Extract common EXIF tags
                    for tag_id, value in exif.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        exif_data[tag] = str(value) if not isinstance(value, (str, int, float)) else value

                    # Extract camera info
                    camera_make = exif_data.get('Make', '').strip()
                    camera_model = exif_data.get('Model', '').strip()

                    return {
                        'camera_make': camera_make,
                        'camera_model': camera_model,
                        'datetime_original': exif_data.get('DateTimeOriginal'),
                        'exif_data': exif_data
                    }

        except Exception as e:
            logger.warning(f"Failed to extract EXIF data: {e}")

        return {
            'camera_make': None,
            'camera_model': None,
            'datetime_original': None,
            'exif_data': {}
        }

    def get_dimensions(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        Get image dimensions.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (width, height) or None if failed
        """
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            logger.error(f"Failed to get image dimensions: {e}")
            return None


# Global image service instance
image_service = ImageService()
