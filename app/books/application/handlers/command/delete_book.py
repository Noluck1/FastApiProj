import logging
from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.domain.access.book_access_subject import BookAccessSubject
from app.books.domain.access.book_access import ensure_can_manage

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class DeleteBookCommand:
    book_id: int
    author: BookAccessSubject


class DeleteBookHandler(IHandler[DeleteBookCommand, BooksDto]):
    def __init__(self, reposytory: IBookRepository, uow: IUnitOfWork):
        self._repository = reposytory
        self._uow = uow


    async def handle(self, request: DeleteBookCommand) -> BooksDto:
        async with self._uow:

            existing_book =  await self._repository.get_book_id(request.book_id)

            ensure_can_manage(
                author=request.author,
                book=existing_book,
            )

            deleted_book_id = await self._repository.delete_book(
                book_id=request.book_id,
                updated_by_id=request.author.user_id,
            )
            await self._uow.commit()

        logger.info(
            "Book deleted: book_id=%s",
            request.book_id,
        )

        return deleted_book_id
        
        