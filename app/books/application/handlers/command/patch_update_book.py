import logging
from dataclasses import dataclass
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.dtos.book_dto import SBooksUpdate, BooksDto
from app.shared.application.port.i_handler import IHandler
from app.books.domain.access.book_access_subject import BookAccessSubject
from app.books.domain.access.book_access import ensure_can_manage

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PatchUpdateBookCommand:
    book_id: int
    book: SBooksUpdate
    author: BookAccessSubject


class PatchUpdateBookHandler(IHandler[PatchUpdateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: PatchUpdateBookCommand) -> BooksDto:
        async with self._uow:

            existing_book = await self._repository.get_book_id(
                book_id=request.book_id
            )

            ensure_can_manage(
                author=request.author,
                book=existing_book
            )

            update_book = await self._repository.patch_update_book(
                book_id=request.book_id,
                book=request.book,
                updated_by_id=request.author.user_id,
            )

            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                request.book_id,
                sorted(request.book.model_fields_set),
            )

            return update_book