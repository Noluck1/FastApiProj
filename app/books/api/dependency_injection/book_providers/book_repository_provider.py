from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.books.infrastructure.persistence.repositories.book.book_repository import BookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


class BookRepositoryProvider(Provider):
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
