from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.books.application.ports.i_book_repository import IBookRepository


@dataclass(frozen=True)
class GetBookIdQuery:
    book_id: int


class GetBookIdHandler(IHandler[GetBookIdQuery, BooksDto]):
    def __init__(self, repository: IBookRepository):
        self._repository = repository


    async def handle(self, request: GetBookIdQuery):
        book = await self._repository.get_book_id(book_id=request.book_id)

        return book
        
         