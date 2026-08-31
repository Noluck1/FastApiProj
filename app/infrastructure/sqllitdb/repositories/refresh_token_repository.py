from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.i_refresh_token_repository import IRefreshTokenRepository
from app.infrastructure.sqllitdb.models.refresh_token_model import RefreshTokenOrm
from app.shared.dtos.auth_dto import RefreshTokenDto


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def add(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshTokenDto:
        token = RefreshTokenOrm(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self._session.add(token)

        await self._session.flush()

        return RefreshTokenDto.model_validate(token)

    async def get_by_hash(
            self, 
            token_hash: str
    ) -> RefreshTokenDto | None:
        result = await self._session.execute(
            select(RefreshTokenOrm).where(
                RefreshTokenOrm.token_hash == token_hash
            )
        )

        token = result.scalar_one_or_none()

        if token is None:
            return None

        return RefreshTokenDto.model_validate(token)

    async def revoke_active(
        self, 
        token_hash: str, 
        revoked_at: datetime,
    ) -> bool:
        result = await self._session.execute(
            update(RefreshTokenOrm)
            .where(
                RefreshTokenOrm.token_hash == token_hash,
                RefreshTokenOrm.revoked_at.is_(None),
                RefreshTokenOrm.expires_at > revoked_at,
            )
            .values(revoked_at=revoked_at)
            .execution_options(synchronize_session=False)
        )

        return result.rowcount == 1
        