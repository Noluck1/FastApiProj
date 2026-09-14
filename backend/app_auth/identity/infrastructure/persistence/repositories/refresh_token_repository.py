from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app_auth.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from backend.app_auth.identity.infrastructure.persistence.models.refresh_token_model import RefreshTokenOrm
from backend.app_auth.identity.infrastructure.persistence.mappers.refresh_session_mapper import refresh_session_to_domain, refresh_session_to_orm
from backend.app_auth.identity.domain.entities.refresh_session import RefreshSession
from backend.app_auth.identity.domain.value_objects.refresh_token_hash import RefreshTokenHash

class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def add(
        self,
        refresh_session: RefreshSession,
    ) -> RefreshSession:
        model = refresh_session_to_orm(
            refresh_session
        )

        self._session.add(model)
        await self._session.flush()

        return refresh_session_to_domain(model)

    async def get_by_hash(
            self, 
            token_hash: RefreshTokenHash,
    ) -> RefreshSession | None:
        result = await self._session.execute(
            select(RefreshTokenOrm).where(
                RefreshTokenOrm.token_hash == token_hash.value
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return refresh_session_to_domain(model)

    async def revoke_active(
        self, 
        token_hash: RefreshTokenHash, 
        revoked_at: datetime,
    ) -> bool:
        result = await self._session.execute(
            update(RefreshTokenOrm)
            .where(
                RefreshTokenOrm.token_hash == token_hash.value,
                RefreshTokenOrm.revoked_at.is_(None),
                RefreshTokenOrm.expires_at > revoked_at,
            )
            .values(revoked_at=revoked_at)
            .execution_options(synchronize_session=False)
        )

        return result.rowcount == 1
        