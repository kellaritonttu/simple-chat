from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class BaseAppSettings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://admin:password@localhost:5432/project"
    FRONTEND_URL: str = "http://localhost:5173"
    FIREBASE_PROJECT_ID: str  = "123"

    model_config = SettingsConfigDict(
        env_file          = os.getenv("ENV_FILE", ".env"),
        env_file_encoding = "utf-8",
        case_sensitive    = True,
        extra             = "ignore",
    )

settings = BaseAppSettings()