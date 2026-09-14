import logging
from dataclasses import dataclass
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_books.books.domain.entities.book_entity.book import Book
from backend.shared.application.port.i_handler import IHandler
from backend.app_books.books.domain.access.book_access_subject import BookAccessSubject
from backend.app_books.books.domain.access.book_access import ensure_can_manage
from backend.app_books.books.domain.exceptions import InvalidBookTitleError
from backend.app_books.books.domain.value_objects.book_value_object.book_title import BookTitle
from backend.app_books.books.domain.value_objects.book_value_object.book_description import BookDescription

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PatchUpdateBookCommand:
    book_id: int
    title: str | None
    description: str | None
    changed_fields: frozenset[str]
    author: BookAccessSubject


class PatchUpdateBookHandler(IHandler[PatchUpdateBookCommand, Book]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: PatchUpdateBookCommand) -> Book:
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
                "Book updated: book_id=%s actor_id=%s "
                "update_type=partial changed_fields=%s",
                saved_book.require_id(),
                request.author.user_id,
                sorted(request.changed_fields),
            )

            return saved_book