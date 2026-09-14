from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app_books.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from backend.app_books.books.infrastructure.persistence.repositories.favorite.favorite_repository import FavoriteRepository


class FavoriteRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def favorite_repository(
        self,
        session: AsyncSession,
    ) -> IFavoriteRepository:
        return FavoriteRepository(session)
