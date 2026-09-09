from abc import ABC, abstractmethod
from datetime import datetime
from app_books.books.shared.dto.book_list import BookListFilters, BookListSortBy, SortOrder
from app_books.books.domain.entities.book_entity.book import Book

class IBookRepository(ABC):
    @abstractmethod
    async def add_book(self, book: Book) -> Book:
        raise NotImplementedError

    @abstractmethod
    async def get_books(
        self, 
        *,
        page: int,
        page_size: int,
        filters: BookListFilters,
        sort_by: BookListSortBy,
        sort_order: SortOrder,
    ) -> tuple[list[Book], int]:
        raise NotImplementedError

    @abstractmethod
    async def get_book_id(self, book_id: int) -> Book:
        raise NotImplementedError

    @abstractmethod
    async def purge_deleted_before(self, cutoff: datetime) -> int:
        raise NotImplementedError

    @abstractmethod
    async def save(self, book: Book) -> Book:
        raise NotImplementedError