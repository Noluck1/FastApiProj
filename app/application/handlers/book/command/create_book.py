from dataclasses import dataclass
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.application.repositories.i_book_repository import IBookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_access import IBookAccess
from app.shared.dtos.book_dto import SBooksAdd
from app.shared.dtos.auth_dto import UserDto
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CreateBookCommand:
    book: SBooksAdd
    current_user: UserDto


class CreateBookHandler(IHandler[CreateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork, book_access: IBookAccess):
        self._repository = repository
        self._uow = uow
        self._book_access = book_access

    async def handle(self, request: CreateBookCommand) -> BooksDto:

        async with self._uow:
            created_book = await self._repository.add_book(
                book=request.book, 
                author_id=request.current_user.id
            )

            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s author_id=%s",
                created_book.id,
                request.current_user.id,
            )

        return created_book
        


