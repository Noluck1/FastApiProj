from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.repositories.i_book_repository import IBookRepository
from app.infrastructure.sqllitdb.repositories.book_repository import BookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.infrastructure.sqllitdb.unit_of_work import UnitOfWork



class RepositoryProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def book_repository(
        self,
        session: AsyncSession,
    ) -> IBookRepository:
        return BookRepository(session)

    @provide
    def unit_of_work(
        self,
        session: AsyncSession
    ) -> IUnitOfWork:
        return UnitOfWork(session)