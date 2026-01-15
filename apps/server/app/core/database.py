import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global MongoDB client
mongo_client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """Connect to MongoDB with retry logic."""
    global mongo_client

    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to MongoDB (attempt {attempt + 1}/{max_retries})...")
            mongo_client = AsyncIOMotorClient(settings.mongodb_url)

            # Test connection
            await mongo_client.admin.command('ping')

            logger.info("Successfully connected to MongoDB")
            return

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not connect to MongoDB.")
                raise


async def init_db():
    """Initialize Beanie with document models."""
    try:
        # Import document models here to avoid circular imports
        from app.models.user import User
        # from app.models.photo import Photo
        # from app.models.collection import Collection

        database = mongo_client[settings.mongodb_db_name]

        # Initialize Beanie with document models
        await init_beanie(
            database=database,
            document_models=[
                User,
                # Photo,
                # Collection,
                # Add more models as they are created
            ]
        )

        logger.info("Beanie initialized successfully")

        # Create default admin user if not exists
        await create_default_admin()

    except Exception as e:
        logger.error(f"Failed to initialize Beanie: {e}")
        raise


async def create_default_admin():
    """Create default admin user if none exists."""
    from app.models.user import get_user_by_username, create_user

    try:
        # Check if any admin user exists
        admin = await get_user_by_username("admin")

        if not admin:
            # Create default admin user
            # IMPORTANT: Change this password in production!
            default_password = "admin123456"
            await create_user("admin", default_password)
            logger.warning(
                "Default admin user created. Username: admin, Password: %s. "
                "Please change this password immediately!",
                default_password
            )
        else:
            logger.info("Admin user already exists")

    except Exception as e:
        logger.error(f"Failed to create default admin user: {e}")


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongo_client

    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB connection closed")
