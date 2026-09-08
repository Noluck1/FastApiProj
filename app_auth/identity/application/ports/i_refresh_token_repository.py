from abc import ABC, abstractmethod
from datetime import datetime
from app_auth.identity.domain.value_objects.refresh_token_hash import RefreshTokenHash
from app_auth.identity.domain.entities.refresh_session import RefreshSession


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def add(
        self,
        session: RefreshSession,
    ) -> RefreshSession:
        raise NotImplementedError

    @abstractmethod
    async def get_by_hash(
        self,
        token_hash: RefreshTokenHash,
    ) -> RefreshSession | None:
        raise NotImplementedError

    @abstractmethod
    async def revoke_active(
        self,
        token_hash: RefreshTokenHash,
        revoked_at: datetime,
    ) -> bool:
        raise NotImplementedError