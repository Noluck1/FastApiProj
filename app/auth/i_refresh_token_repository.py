from abc import ABC, abstractmethod
from datetime import datetime
from app.shared.dtos.auth_dto import RefreshTokenDto

class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def add(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshTokenDto:
        raise NotImplementedError

    @abstractmethod
    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshTokenDto | None:
        raise NotImplementedError

    @abstractmethod
    async def revoke_active(
        self,
        token_hash: str,
        revoked_at: datetime,
    ) -> bool:
        raise NotImplementedError