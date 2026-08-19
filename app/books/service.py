from app.shared.dtos.book_dto import SBooksUpdate, SBooksAdd
from app.books.unit_of_work import UnitOfWork


class BookService:
    async def add_book(self, book: SBooksAdd) -> int:
        async with UnitOfWork() as uow:
            book_id = await uow.books.add_book(book)
            await uow.commit()
            return book_id

    async def get_books(self):
        async with UnitOfWork() as uow:
            return await uow.books.get_books()

    async def get_book_id(self, book_id: int):
        async with UnitOfWork() as uow:
            return await uow.books.get_book_id(book_id)

    async def update_book(self, book_id: int, book: SBooksUpdate):
        async with UnitOfWork() as uow:
            update_book = await uow.books.update_book(book_id, book)
            await uow.commit()
            return update_book

    async def delete_book(self, book_id: int):
        async with UnitOfWork() as uow:
            deleted_book_id = await uow.books.delete_book(book_id)

            await uow.commit()

            return deleted_book_id