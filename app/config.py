import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Password_database Central IdP"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "production"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8020

    SECRET_KEY: str = "central-identity-super-secret-key-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = "sqlite:///./password_database.db"
    MASTER_API_KEY: str = "master-internal-auth-key-2026"
    CORS_ORIGINS: str = "https://thesis.manamatechnologies.com,https://libraryapp.manamatechnologies.com,http://localhost:3000,http://localhost:5173"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
