from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.repositories.i_book_repository import IBookRepository
from app.auth.i_user_repository import IUserRepository
from app.infrastructure.sqllitdb.repositories.book_repository import BookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.infrastructure.sqllitdb.repositories.user_repository import UserRepository
from app.infrastructure.sqllitdb.unit_of_work import UnitOfWork
from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.infrastructure.sqllitdb.repositories.favorite_repository import FavoriteRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def user_repository(
        self,
        session: AsyncSession
    ) -> IUserRepository:
        return UserRepository(session)

    @provide
    def book_repository(
        self,
        session: AsyncSession,
    ) -> IBookRepository:
        return BookRepository(session)

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
