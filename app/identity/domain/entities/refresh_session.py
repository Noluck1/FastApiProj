from dataclasses import dataclass
from datetime import datetime

from app.identity.domain.value_objects.refresh_token_hash import RefreshTokenHash


@dataclass(slots=True)
class RefreshSession:
    id: int | None
    user_id: int 
    token_hash: RefreshTokenHash
    expires_at: datetime
    revoked_at: datetime | None = None

    def is_expired(self, now: datetime) -> bool:
        return self.expires_at <= now

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_active(self, now: datetime) -> bool:
        return not self.is_revoked() and not self.is_expired(now)

    def revoke(self, now: datetime) -> None:
        self.revoked_at = now