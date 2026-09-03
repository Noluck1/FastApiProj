from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork
from app.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from app.books.infrastructure.persistence.repositories.favorite.favorite_repository import FavoriteRepository


class FavoriteRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def favorite_repository(
        self,
        session: AsyncSession,
    ) -> IFavoriteRepository:
        return FavoriteRepository(session)

    @provide
    def unit_of_work(
        self,
        session: AsyncSession
    ) -> IUnitOfWork:
        return UnitOfWork(session)