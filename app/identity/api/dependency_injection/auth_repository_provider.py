from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from app.identity.infrastructure.persistence.repositories.refresh_token_repository import RefreshTokenRepository
from app.identity.application.ports.i_user_repository import IUserRepository
from app.identity.infrastructure.persistence.repositories.user_repository import UserRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork

class AuthRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repository(
        self,
        session: AsyncSession
    ) -> IUserRepository:
        return UserRepository(session)

    @provide
    def unit_of_work(
        self,
        session: AsyncSession
    ) -> IUnitOfWork:
        return UnitOfWork(session)

    @provide
    def refresh_token_repository(
        self,
        session: AsyncSession,
    ) -> IRefreshTokenRepository:
        return RefreshTokenRepository(session)