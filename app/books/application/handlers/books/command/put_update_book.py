import logging
from dataclasses import dataclass
from app.books.api.dto.book.book_dto import BooksDto
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.application.port.i_handler import IHandler
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.books.domain.access.book_access_subject import BookAccessSubject
from app.books.domain.access.book_access import ensure_can_manage
from app.books.domain.entities.book_entity.book import Book
from app.books.domain.value_objects.book_value_object.book_title import BookTitle
from app.books.domain.value_objects.book_value_object.book_description import BookDescription
from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.books.application.exceptions import ReferencedUserNotFoundError


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PutUppdateBookCommand:
    book_id: int
    title: str
    description: str | None
    author: BookAccessSubject


class PutUppdateBookHandler(IHandler[PutUppdateBookCommand, Book]):
    def __init__(
            self, 
            repository: IBookRepository, 
            uow: IUnitOfWork,
            user_checker: IIdentityCommunication,
    ):
        self._repository = repository
        self._uow = uow
        self._user_checker = user_checker

    async def handle(self, request: PutUppdateBookCommand) -> Book:
        async with self._uow:

            user_exists = await self._user_checker.get_active_user(request.author.user_id)

            if not user_exists:
                raise ReferencedUserNotFoundError(user_id=request.author.user_id)

            book = await self._repository.get_book_id(
                request.book_id
            )

            ensure_can_manage(
                author=request.author,
                book=book
            )

            book.change_title(
                title=BookTitle(request.title),
                updated_by_id=request.author.user_id,
            )

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
                "Book updated: book_id=%s",
                saved_book.require_id(),
            )   

            return saved_book