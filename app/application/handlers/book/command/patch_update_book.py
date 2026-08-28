import logging
from dataclasses import dataclass
from app.application.repositories.i_book_repository import IBookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.shared.dtos.book_dto import SBooksUpdate, BooksDto
from app.shared.dtos.auth_dto import UserDto
from app.application.handlers.i_handler import IHandler

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PatchUpdateBookCommand:
    book_id: int
    book: SBooksUpdate
    current_user: UserDto


class PatchUpdateBookHandler(IHandler[PatchUpdateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: PatchUpdateBookCommand) -> BooksDto:
        async with self._uow:
            existing_book = await self._repository.get_book_id(
                book_id=request.book_id
            )

            self._repository.ensure_can_manage(
                user=request.current_user,
                book=existing_book
            )

            update_book = await self._repository.patch_update_book(
                book_id=request.book_id,
                book=request.book,
                updated_by_id=request.current_user.id
            )

            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                request.book_id,
                sorted(request.book.model_fields_set),
            )

            return update_book