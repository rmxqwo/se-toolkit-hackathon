from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/resume_builder"

    # Qwen API
    QWEN_API_KEY: str = ""
    QWEN_MODEL: str = "qwen-plus"

    # Application
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30

    # PDF
    PDF_DEFAULT_FONT: str = "Helvetica"
    PDF_PAGE_SIZE: str = "A4"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()


settings = get_settings()
