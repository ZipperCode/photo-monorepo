"""Photo upload API endpoints."""

from typing import List
from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from pydantic import BaseModel

from app.services.photo_service import photo_service

router = APIRouter()


class UploadResult(BaseModel):
    """Result of photo upload operation."""
    success: bool
    filename: str
    photo_id: str | None = None
    file_size: int | None = None
    error: str | None = None


class UploadResponse(BaseModel):
    """Response for photo upload endpoint."""
    uploaded: List[UploadResult]
    failed: List[UploadResult]
    total: int
    success_count: int
    failed_count: int


@router.post(
    "/collections/{code}/photos",
    response_model=UploadResponse,
    summary="Upload photos to collection",
    description="Upload one or more photos to a collection using its access code"
)
async def upload_photos(
    code: str,
    request: Request,
    files: List[UploadFile] = File(...)
):
    """
    Upload photos to a collection.

    Args:
        code: Collection access code
        request: FastAPI request object
        files: List of uploaded files

    Returns:
        Upload results with success/failure details
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Get uploader info
    uploader_info = {
        'ip_address': request.client.host if request.client else None,
        'user_agent': request.headers.get('user-agent')
    }

    # Process uploads
    results = []
    for file in files:
        result = await photo_service.upload_photo(
            file=file,
            collection_code=code,
            uploader_info=uploader_info
        )
        results.append(UploadResult(**result))

    # Separate successful and failed uploads
    uploaded = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    return UploadResponse(
        uploaded=uploaded,
        failed=failed,
        total=len(results),
        success_count=len(uploaded),
        failed_count=len(failed)
    )
