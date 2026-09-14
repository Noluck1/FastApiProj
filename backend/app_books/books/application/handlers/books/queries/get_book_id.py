import logging
from dataclasses import dataclass
from backend.shared.application.port.i_handler import IHandler
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.app_books.books.domain.entities.book_entity.book import Book

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class GetBookIdQuery:
    book_id: int


class GetBookIdHandler(IHandler[GetBookIdQuery, Book]):
    def __init__(self, repository: IBookRepository):
        self._repository = repository


    async def handle(self, request: GetBookIdQuery) -> Book:
        book = await self._repository.get_book_id(book_id=request.book_id)

        logger.debug(
            "Book: book_id=%s",
            book.require_id(),
        )

        return book
        
         