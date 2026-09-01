from dataclasses import dataclass
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.application.repositories.i_book_repository import IBookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.shared.dtos.book_dto import SBooksAdd
import logging
from app.domain.auth.entities.user import User

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CreateBookCommand:
    book: SBooksAdd
    current_user: User


class CreateBookHandler(IHandler[CreateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow


    async def handle(self, request: CreateBookCommand) -> BooksDto:
        user_id = request.current_user.require_id()

        async with self._uow:
            
            created_book = await self._repository.add_book(
                book=request.book, 
                author_id=user_id
            )

            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s author_id=%s",
                created_book.id,
                user_id,
            )

        return created_book
        


