from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Photo Collection System"
    environment: str = "development"

    # MongoDB
    mongodb_url: str
    mongodb_db_name: str = "photo_system"

    # Storage
    storage_type: str = "local"
    storage_path: str = "./storage"

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 1440  # 24 hours

    # CORS
    cors_origins: str = '["http://localhost:5173","http://localhost:5174"]'

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
