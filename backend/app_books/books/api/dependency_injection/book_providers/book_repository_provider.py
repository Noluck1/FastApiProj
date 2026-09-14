from  dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.app_books.books.infrastructure.persistence.repositories.book.book_repository import BookRepository

class BookRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def book_repository(
        self,
        session: AsyncSession,
    ) -> IBookRepository:
        return BookRepository(session)
