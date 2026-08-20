from app.shared.dtos.book_dto import SBooksUpdate, SBooksAdd
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_repository import IBookRepository


class BookService:
    def __init__(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ):
        self._repository = repository
        self._uow = uow
        


    async def add_book(self, book: SBooksAdd):
        async with self._uow:
            book_id = await self._repository.add_book(book)
            await self._uow.commit()
            return book_id

    async def get_books(self):
        async with self._uow:
            return await self._repository.get_books()

    async def get_book_id(self, book_id: int):
        async with self._uow:
            return await self._repository.get_book_id(book_id)

    async def update_book(self, book_id: int, book: SBooksUpdate):
        async with self._uow:
            update_book = await self._repository.update_book(book_id, book)
            await self._uow.commit()
            return update_book

    async def delete_book(self, book_id: int):
        async with self._uow:
            deleted_book_id = await self._repository.delete_book(book_id)

            await self._uow.commit()

            return deleted_book_id