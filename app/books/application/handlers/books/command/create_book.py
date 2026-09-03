import logging
from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.domain.entities.book_entity.book import Book
from app.books.domain.value_objects.book_value_object.book_title import BookTitle
from app.books.domain.value_objects.book_value_object.book_description import BookDescription
from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.books.application.exceptions import ReferencedUserNotFoundError


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CreateBookCommand:
    title: str
    description: str | None
    author_id: int


class CreateBookHandler(IHandler[CreateBookCommand, Book]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork, user_checker: IIdentityCommunication):
        self._repository = repository
        self._uow = uow
        self._user_checker = user_checker


    async def handle(self, request: CreateBookCommand) -> Book:
        async with self._uow:

            user_exists = await self._user_checker.get_active_user(request.author_id)

            if not user_exists:
                raise ReferencedUserNotFoundError(user_id=request.author_id)

            book = Book(
                id=None,
                title=BookTitle(request.title),
                description=(
                    BookDescription(request.description)
                    if request.description is not None
                    else None
                ),
                author_id=request.author_id,
            )
            
            created_book = await self._repository.add_book(book)

            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s author_id=%s",
                created_book.id,
                request.author_id,
            )

        return created_book
        


