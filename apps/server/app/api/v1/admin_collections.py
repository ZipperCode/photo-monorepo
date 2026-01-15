"""Admin collection API endpoints.

This module provides endpoints for managing collections (CRUD operations).
All endpoints require authentication via JWT token.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.collection import (
    Collection,
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    get_collection_by_code,
    create_collection,
    list_collections,
    update_collection,
    delete_collection,
    count_collections
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin/collections", tags=["admin-collections"])


@router.post(
    "",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create collection",
    description="Create a new collection with auto-generated unique code."
)
async def create_collection_endpoint(
    data: CollectionCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new photo collection.

    A unique 6-character code will be automatically generated.
    The collection will be associated with the current admin user.

    ## Request Body
    - name: Collection name (3-100 characters, required)
    - description: Optional description
    - status: Collection status (default: "active")
    - settings: Optional upload settings

    ## Example
    ```bash
    curl -X POST http://localhost:8000/api/v1/admin/collections \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Wedding Photos",
        "description": "John & Jane Wedding",
        "status": "active"
      }'
    ```

    ## Response
    Returns the created collection with auto-generated code.
    """
    try:
        collection = await create_collection(data, created_by=current_user.username)
        return CollectionResponse(
            id=str(collection.id),
            code=collection.code,
            name=collection.name,
            description=collection.description,
            status=collection.status,
            settings=collection.settings,
            statistics=collection.statistics,
            created_at=collection.created_at,
            created_by=collection.created_by
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[CollectionResponse],
    summary="List collections",
    description="Get paginated list of collections with optional status filter."
)
async def list_collections_endpoint(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (active/archived/closed)"),
    current_user: User = Depends(get_current_user)
):
    """
    List all collections with pagination.

    ## Query Parameters
    - page: Page number (default: 1, min: 1)
    - limit: Items per page (default: 20, min: 1, max: 100)
    - status: Optional status filter

    ## Example
    ```bash
    curl -X GET "http://localhost:8000/api/v1/admin/collections?page=1&limit=20" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

    ## Response
    Returns array of collections sorted by creation date (newest first).
    """
    # Validate status filter if provided
    if status:
        allowed_statuses = {"active", "archived", "closed"}
        if status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of {allowed_statuses}"
            )

    skip = (page - 1) * limit
    collections = await list_collections(skip=skip, limit=limit, status_filter=status)

    return [
        CollectionResponse(
            id=str(c.id),
            code=c.code,
            name=c.name,
            description=c.description,
            status=c.status,
            settings=c.settings,
            statistics=c.statistics,
            created_at=c.created_at,
            created_by=c.created_by
        )
        for c in collections
    ]


@router.get(
    "/{code}",
    response_model=CollectionResponse,
    summary="Get collection by code",
    description="Get detailed information about a specific collection."
)
async def get_collection_endpoint(
    code: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific collection by its code.

    ## Path Parameters
    - code: 6-character collection code (case-insensitive)

    ## Example
    ```bash
    curl -X GET http://localhost:8000/api/v1/admin/collections/ABC123 \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

    ## Response
    Returns collection details or 404 if not found.
    """
    collection = await get_collection_by_code(code)

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )

    return CollectionResponse(
        id=str(collection.id),
        code=collection.code,
        name=collection.name,
        description=collection.description,
        status=collection.status,
        settings=collection.settings,
        statistics=collection.statistics,
        created_at=collection.created_at,
        created_by=collection.created_by
    )


@router.patch(
    "/{code}",
    response_model=CollectionResponse,
    summary="Update collection",
    description="Update collection details (partial update)."
)
async def update_collection_endpoint(
    code: str,
    data: CollectionUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing collection.

    Only provided fields will be updated. The collection code cannot be changed.

    ## Request Body
    All fields are optional:
    - name: New collection name
    - description: New description
    - status: New status (active/archived/closed)
    - settings: New settings object

    ## Example
    ```bash
    curl -X PATCH http://localhost:8000/api/v1/admin/collections/ABC123 \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"status": "archived"}'
    ```

    ## Response
    Returns updated collection or 404 if not found.
    """
    collection = await update_collection(code, data)

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )

    return CollectionResponse(
        id=str(collection.id),
        code=collection.code,
        name=collection.name,
        description=collection.description,
        status=collection.status,
        settings=collection.settings,
        statistics=collection.statistics,
        created_at=collection.created_at,
        created_by=collection.created_by
    )


@router.delete(
    "/{code}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete collection",
    description="Soft delete a collection (marks as deleted, preserves data)."
)
async def delete_collection_endpoint(
    code: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a collection (soft delete).

    The collection is marked as deleted but preserved in the database
    for audit purposes. To permanently delete, use database admin tools.

    ## Path Parameters
    - code: 6-character collection code

    ## Example
    ```bash
    curl -X DELETE http://localhost:8000/api/v1/admin/collections/ABC123 \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

    ## Response
    Returns 204 No Content on success, 404 if not found.
    """
    success = await delete_collection(code)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )

    return None


@router.get(
    "/stats/count",
    summary="Get collection statistics",
    description="Get count of collections, optionally filtered by status."
)
async def get_collection_count(
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_user)
):
    """
    Get count of collections.

    ## Query Parameters
    - status: Optional status filter (active/archived/closed)

    ## Example
    ```bash
    curl -X GET "http://localhost:8000/api/v1/admin/collections/stats/count" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

    ## Response
    ```json
    {
      "total": 42,
      "active": 38,
      "archived": 3,
      "closed": 1
    }
    ```
    """
    if status:
        count = await count_collections(status_filter=status)
        return {"total": count}

    # Return counts for all statuses if no filter
    total = await count_collections()
    active = await count_collections(status_filter="active")
    archived = await count_collections(status_filter="archived")
    closed = await count_collections(status_filter="closed")

    return {
        "total": total,
        "active": active,
        "archived": archived,
        "closed": closed
    }
