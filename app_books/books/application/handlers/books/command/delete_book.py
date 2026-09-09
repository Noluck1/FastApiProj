import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from shared.application.port.i_handler import IHandler
from app_books.books.domain.entities.book_entity.book import Book
from app_books.books.application.ports.book.i_book_repository import IBookRepository
from shared.application.port.i_unit_of_work import IUnitOfWork
from app_books.books.domain.access.book_access_subject import BookAccessSubject
from app_books.books.domain.access.book_access import ensure_can_manage

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class DeleteBookCommand:
    book_id: int
    author: BookAccessSubject


class DeleteBookHandler(IHandler[DeleteBookCommand, Book]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: DeleteBookCommand) -> Book:
        async with self._uow:

            book =  await self._repository.get_book_id(request.book_id)

            ensure_can_manage(
                author=request.author,
                book=book,
            )

            book.delete(
                updated_by_id=request.author.user_id,
                deleted_at=datetime.now(timezone.utc),
            )

            saved_book = await self._repository.save(book)

            await self._uow.commit()

        logger.info(
            "Book soft deleted: book_id=%s actor_id=%s",
            saved_book.require_id(),
            request.author.user_id,
        )

        return saved_book
        
        