import logging
from app.shared.dtos.book_dto import SBooksUpdate, SBooksAdd
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_repository import IBookRepository
from app.shared.dtos.book_dto import BooksDto

logger = logging.getLogger(__name__)

class BookService:
    def __init__(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow
        


    async def add_book(
            self, 
            book: SBooksAdd
    ) -> BooksDto:
        async with self._uow:
            created_book = await self._repository.add_book(book)
            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s",
                created_book.id,
            )

            return created_book

    async def get_books(self) -> list[BooksDto]:
        async with self._uow:

            return await self._repository.get_books()

    async def get_book_id(
            self, 
            book_id: int
    ) -> BooksDto:
        async with self._uow:

            return await self._repository.get_book_id(book_id)

    async def update_book(
            self, 
            book_id: int, 
            book: SBooksUpdate
    ) -> BooksDto:
        async with self._uow:
            update_book = await self._repository.update_book(book_id, book)
            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                book_id,
                sorted(book.model_fields_set),
            )

            return update_book

    async def delete_book(
            self, 
            book_id: int
    ) -> BooksDto:
        async with self._uow:
            deleted_book_id = await self._repository.delete_book(book_id)
            await self._uow.commit()

            logger.info(
                "Book deleted: book_id=%s",
                book_id,
            )

            return deleted_book_id