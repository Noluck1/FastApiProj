import logging
from dataclasses import dataclass
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.api.dto.book_dto import SBooksUpdate, BooksDto
from app.shared.application.port.i_handler import IHandler
from app.books.domain.access.book_access_subject import BookAccessSubject
from app.books.domain.access.book_access import ensure_can_manage
from app.books.domain.exceptions import InvalidBookTitleError
from app.books.domain.value_objects.book_title import BookTitle
from app.books.domain.value_objects.book_description import BookDescription

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PatchUpdateBookCommand:
    book_id: int
    title: str | None
    description: str | None
    changed_fields: frozenset[str]
    author: BookAccessSubject


class PatchUpdateBookHandler(IHandler[PatchUpdateBookCommand, BooksDto]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: PatchUpdateBookCommand) -> BooksDto:
        async with self._uow:

            book = await self._repository.get_book_id(
               request.book_id
            )

            ensure_can_manage(
                author=request.author,
                book=book
            )

            if "title" in request.changed_fields:
                if request.title is None:
                    raise InvalidBookTitleError

                book.change_title(
                    title=BookTitle(request.title),
                    updated_by_id=request.author.user_id,
                )

            if "description" in request.changed_fields:
                book.change_description(
                    description=(
                        BookDescription(request.description)
                        if request.description is not None
                        else None
                    ),
                    updated_by_id=request.author.user_id,
                )

            saved_book = await self._repository.save(book)
            
            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                request.book_id,
            )

            return saved_book