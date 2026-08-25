from abc import ABC, abstractmethod
from datetime import datetime
from app.shared.dtos.book_dto import SBooksAdd, BooksDto, SBooksUpdate

class IBookRepository(ABC):
    @abstractmethod
    async def add_book(self, book: SBooksAdd, author_id: int) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def get_books(self) -> list[BooksDto]:
        raise NotImplementedError

    @abstractmethod
    async def get_book_id(self, book_id: int) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def update_book(self, book_id: int, book: SBooksUpdate) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def delete_book(self, book_id: int) -> BooksDto:
        raise NotImplementedError


    @abstractmethod
    async def purge_deleted_before(self, cutoff: datetime) -> int:
        raise NotImplementedError