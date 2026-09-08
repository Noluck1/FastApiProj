from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app_auth.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from app_auth.identity.infrastructure.persistence.repositories.refresh_token_repository import RefreshTokenRepository
from app_auth.identity.application.ports.i_user_repository import IUserRepository
from app_auth.identity.infrastructure.persistence.repositories.user_repository import UserRepository

class AuthRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repository(
        self,
        session: AsyncSession
    ) -> IUserRepository:
        return UserRepository(session)

    @provide
    def refresh_token_repository(
        self,
        session: AsyncSession,
    ) -> IRefreshTokenRepository:
        return RefreshTokenRepository(session)