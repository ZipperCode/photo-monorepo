"""API v1 module."""

from fastapi import APIRouter

from app.api.v1 import auth, collections, admin_collections, photos

# Create API v1 router
api_router = APIRouter(prefix="/api/v1")

# Include sub-routers
api_router.include_router(auth.router)
api_router.include_router(collections.router)  # Public endpoints
api_router.include_router(admin_collections.router)  # Admin endpoints
api_router.include_router(photos.router)  # Photo upload endpoints

# Export router for main app
__all__ = ["api_router"]
