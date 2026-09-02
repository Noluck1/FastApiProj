from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.dtos.book_dto import SBooksAdd
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CreateBookCommand:
    book: SBooksAdd
    author_id: int


class CreateBookHandler(IHandler[CreateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow


    async def handle(self, request: CreateBookCommand) -> BooksDto:
        async with self._uow:
            
            created_book = await self._repository.add_book(
                book=request.book, 
                author_id=request.author_id
            )

            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s author_id=%s",
                created_book.id,
                request.author_id,
            )

        return created_book
        


