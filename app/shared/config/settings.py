from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    log_level: str = "INFO"

    book_cleanup_retention_minutes: int = Field(default=30, gt=0)
    book_cleanup_interval_seconds: int = Field(default=1, gt=0)

    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    jwt_issuer: str = "books-api"
    jwt_audience: str = "books-api-users"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()