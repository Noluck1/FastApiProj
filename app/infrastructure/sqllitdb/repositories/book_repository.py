from fastapi import HTTPException
from sqlalchemy import select
from app.infrastructure.sqllitdb.models.book_model import BooksOrm
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate
from app.books.exceptions import NotFoundError

class BookRepository:
    def __init__(self, session):
        self.session = session

    async def add_book(self, book: SBooksAdd) -> int:
        data = book.model_dump()
        new_book = BooksOrm(**data)

        self.session.add(new_book)
        await self.session.flush()

        return new_book.title


    async def get_books(self):
        result = await self.session.execute(select(BooksOrm))
        books = result.scalars().all()

        return books



    async def get_book_id(self, book_id: int):
        result = await self.session.execute(select(BooksOrm).where(BooksOrm.id == book_id))
        book = result.scalar_one_or_none()

        if book is None:
            raise NotFoundError(id=book_id)

        return book


    async def update_book(self, book_id: int, book: SBooksUpdate):
        book_model = await self.get_book_id(book_id)

        data = book.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(book_model, key, value)

        await self.session.flush()

        return book_model

    async def delete_book(self, book_id: int):
        book_model = await self.get_book_id(book_id)

        await self.session.delete(book_model)

        return book_model