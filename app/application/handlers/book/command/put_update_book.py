import logging
from dataclasses import dataclass
from app.shared.dtos.book_dto import SPutBookUpdate, BooksDto
from app.shared.dtos.auth_dto import UserDto
from app.application.i_unit_of_work import IUnitOfWork
from app.application.handlers.i_handler import IHandler
from app.application.repositories.i_book_repository import IBookRepository

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PutUppdateBookCommand:
    book_id: int
    book: SPutBookUpdate
    current_user: UserDto


class PutUppdateBookHandler(IHandler[PutUppdateBookCommand, BooksDto]):
    def __init__(
            self, 
            repository: IBookRepository, 
            uow: IUnitOfWork,
    ):
        self._repository = repository
        self._uow = uow


    async def handle(self, reauest: PutUppdateBookCommand) -> BooksDto:
        async with self._uow:
            existing_book = await self._repository.get_book_id(
                reauest.book_id
            )

            self._repository.ensure_can_manage(
                user=reauest.current_user,
                book=existing_book
            )

            update_book = await self._repository.put_update_book(
                book_id=reauest.book_id,
                book=reauest.book,
                updated_by_id=reauest.current_user.id,
            )

            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                reauest.book_id,
                sorted(reauest.book.model_fields_set),
            )

            return update_book