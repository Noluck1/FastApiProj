from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[3]

class IdentitySettings(BaseSettings):
    database_url: str
    log_level: str = "INFO"

    jwt_private_key_path: Path
    jwt_public_key_path: Path
    jwt_algorithm: str = "RS256"
    jwt_issuer: str = "identity-service"
    jwt_audience: str = "books-api"
    access_token_expire_minutes: int = 15

    internal_service_token: SecretStr

    refresh_token_expire_days: int = 30
    refresh_cookie_secure: bool = True

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_prefix="IDENTITY_",
        extra="ignore",
    )


identity_settings = IdentitySettings()