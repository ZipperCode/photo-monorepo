"""Public collection API endpoints.

This module provides endpoints that can be accessed without authentication,
primarily for users to validate collection codes before uploading photos.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.collection import (
    ValidateCodeRequest,
    ValidateCodeResponse,
    get_collection_by_code
)

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post(
    "/validate",
    response_model=ValidateCodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate collection code",
    description="Validate a 6-character collection code and return collection details if valid."
)
async def validate_collection_code(request: ValidateCodeRequest):
    """
    Validate a collection code without requiring authentication.

    This endpoint is used by users to verify that a collection code is valid
    and active before being allowed to upload photos.

    ## Validation Rules
    - Code must be exactly 6 characters (case-insensitive)
    - Code must exist in database
    - Collection status must be "active"
    - Collection must have allow_upload setting enabled

    ## Response
    - Returns valid=True with collection details if code is valid
    - Returns valid=False with error message if code is invalid, inactive, or not accepting uploads

    ## Examples
    ```bash
    # Valid code
    curl -X POST http://localhost:8000/api/v1/collections/validate \
      -H "Content-Type: application/json" \
      -d '{"code": "ABC123"}'

    # Response: {"valid": true, "collection": {...}}

    # Invalid code
    curl -X POST http://localhost:8000/api/v1/collections/validate \
      -H "Content-Type: application/json" \
      -d '{"code": "INVALID"}'

    # Response: {"valid": false, "message": "Collection code not found"}
    ```
    """
    # Normalize code to uppercase
    code = request.code.strip().upper()

    # Check if collection exists
    collection = await get_collection_by_code(code)

    if not collection:
        return ValidateCodeResponse(
            valid=False,
            message="Collection code not found. Please check the code and try again."
        )

    # Check if collection is active
    if collection.status != "active":
        status_messages = {
            "archived": "This collection has been archived and is no longer accepting uploads.",
            "closed": "This collection is closed and no longer accepting uploads."
        }
        return ValidateCodeResponse(
            valid=False,
            message=status_messages.get(
                collection.status,
                f"This collection is {collection.status}."
            )
        )

    # Check if uploads are allowed
    allow_upload = collection.settings.get("allow_upload", True)
    if not allow_upload:
        return ValidateCodeResponse(
            valid=False,
            message="Upload is not currently allowed for this collection."
        )

    # Code is valid - return collection details
    return ValidateCodeResponse(
        valid=True,
        collection={
            "code": collection.code,
            "name": collection.name,
            "description": collection.description,
            "settings": {
                "max_file_size": collection.settings.get("max_file_size", 10 * 1024 * 1024),
                "allowed_extensions": collection.settings.get("allowed_extensions", [])
            }
        }
    )
