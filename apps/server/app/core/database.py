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
        # from app.models.photo import Photo
        # from app.models.user import User

        database = mongo_client[settings.mongodb_db_name]

        # Initialize Beanie with document models
        await init_beanie(
            database=database,
            document_models=[
                # Photo,
                # User,
                # Add more models as they are created
            ]
        )

        logger.info("Beanie initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Beanie: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongo_client

    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB connection closed")
