from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.books.domain.entities.book_entity.book import Book


@dataclass(frozen=True)
class GetBookIdQuery:
    book_id: int


class GetBookIdHandler(IHandler[GetBookIdQuery, Book]):
    def __init__(self, repository: IBookRepository):
        self._repository = repository


    async def handle(self, request: GetBookIdQuery) -> Book:
        book = await self._repository.get_book_id(book_id=request.book_id)

        return book
        
         