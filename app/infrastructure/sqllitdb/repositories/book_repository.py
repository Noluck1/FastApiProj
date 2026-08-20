from fastapi import HTTPException
from sqlalchemy import select
from app.infrastructure.sqllitdb.models.book_model import BooksOrm
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate, SBooks, BooksDto
from app.application.exceptions import NotFoundError
from app.application.repositories.i_book_repository import IBookRepository

class BookRepository(IBookRepository):
    def __init__(self, session):
        self.session = session

    async def add_book(self, book: SBooksAdd) -> BooksDto:
        data = book.model_dump()
        new_book = BooksOrm(**data)

        self.session.add(new_book)
        await self.session.flush()

        return BooksDto.model_validate(new_book)


    async def get_books(self) -> list[BooksDto]:
        result = await self.session.execute(select(BooksOrm))
        books = result.scalars().all()

        if not books:
            raise NotFoundError(id=books)

        return [BooksDto.model_validate(book) for book in books]


    async def _get_model_by_id(self, book_id: int) -> BooksOrm:
        book_model = await self.session.get(BooksOrm, book_id)

        if book_model is None:
            raise NotFoundError(id=book_id)

        return book_model



    async def get_book_id(self, book_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)
        return BooksDto.model_validate(book_model)
       


    async def update_book(self, book_id: int, book: SBooksUpdate) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        data = book.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(book_model, key, value)

        await self.session.flush()

        return BooksDto.model_validate(book_model)

    async def delete_book(self, book_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        deleted_book = BooksDto.model_validate(book_model)

        await self.session.delete(book_model)

        return deleted_book