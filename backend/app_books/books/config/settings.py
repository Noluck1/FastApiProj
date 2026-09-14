from pydantic import Field, SecretStr
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class BooksSettings(BaseSettings):
    database_url: str
    log_level: str = "INFO"

    jwt_public_key_path: Path
    jwt_algorithm: str = "RS256"
    jwt_issuer: str = "identity-service"
    jwt_audience: str = "books-api"

    identity_token_url: str = (
        "http://localhost:8001/auth/token"
    )

    identity_base_url: str = "http://localhost:8001"
    identity_service_token: SecretStr
    identity_request_timeout_seconds: float = Field(
        default=3.0,
        gt=0,
    )

    cleanup_retention_days: int = Field(default=30, gt=0)
    cleanup_interval_hours: int = Field(default=1, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BOOKS_",
        extra="ignore",
    )


books_settings = BooksSettings()