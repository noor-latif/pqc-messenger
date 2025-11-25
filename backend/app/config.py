from functools import lru_cache
from typing import List

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ALLOWED_ORIGINS: List[str] = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",
    "http://host.docker.internal:8000",
]


def parse_origins(value: str | None) -> List[str]:
    """Parse allowed origins from comma-separated string."""
    if value is None or not value.strip():
        return DEFAULT_ALLOWED_ORIGINS
    return [origin.strip() for origin in value.split(",") if origin.strip()]


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    # Store as string to prevent Pydantic Settings from trying to JSON-decode
    allowed_origins_str: str | None = Field(
        default=None, alias="ALLOWED_ORIGINS", exclude=True
    )

    @computed_field
    @property
    def allowed_origins(self) -> List[str]:
        """Parse allowed origins from string or return defaults."""
        return parse_origins(self.allowed_origins_str)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()


