"""API v1 module."""

from fastapi import APIRouter

from app.api.v1 import auth

# Create API v1 router
api_router = APIRouter(prefix="/api/v1")

# Include sub-routers
api_router.include_router(auth.router)

# Export router for main app
__all__ = ["api_router"]
