import logging
from dataclasses import dataclass
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.auth_dto import UserDto
from app.shared.dtos.book_dto import BooksDto
from app.application.repositories.i_book_repository import IBookRepository
from app.application.repositories.i_book_access import IBookAccess
from app.application.i_unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class DeleteBookCommand:
    book_id: int
    current_user: UserDto


class DeleteBookHandler(IHandler[DeleteBookCommand, BooksDto]):
    def __init__(self, reposytory: IBookRepository, uow: IUnitOfWork, book_access: IBookAccess):
        self._repository = reposytory
        self._uow = uow
        self._book_access = book_access


    async def handle(self, request: DeleteBookCommand) -> BooksDto:
        async with self._uow:
            existing_book =  await self._repository.get_book_id(request.book_id)

        self._book_access.ensure_can_manage(
            user=request.current_user,
            book=existing_book,
        )

        deleted_book_id = await self._repository.delete_book(
            book_id=request.book_id,
            updated_by_id=request.current_user.id,
        )
        await self._uow.commit()

        logger.info(
            "Book deleted: book_id=%s",
            request.book_id,
        )

        return deleted_book_id
        
        