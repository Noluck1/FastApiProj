import hashlib
import secrets
from datetime import datetime, timedelta, timezone



class RefreshTokenService:
    def __init__(self, expire_days: int) -> None:
        self._expire_days = expire_days
        
    
    def create(self) -> tuple[str, str, datetime]:
        raw_token = secrets.token_urlsafe(48)
        token_hash = self.hash(raw_token)

        expires_at = datetime.now(timezone.utc) + timedelta(days=self._expire_days)

        return raw_token, token_hash, expires_at 

    @staticmethod
    def hash(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    