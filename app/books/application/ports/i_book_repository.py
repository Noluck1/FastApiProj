from abc import ABC, abstractmethod
from datetime import datetime
from app.shared.dtos.book_dto import SBooksAdd, BooksDto, SBooksUpdate, SPutBookUpdate
from app.shared.dtos.book_list import BookListFilters, BookListSortBy, SortOrder

class IBookRepository(ABC):
    @abstractmethod
    async def add_book(self, book: SBooksAdd, author_id: int) -> BooksDto:
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
    ) -> tuple[list[BooksDto], int]:
        raise NotImplementedError

    @abstractmethod
    async def get_book_id(self, book_id: int) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def put_update_book(self, book_id: int, book: SPutBookUpdate, updated_by_id: int) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def patch_update_book(self, book_id: int, book: SBooksUpdate, updated_by_id: int) -> BooksDto:
        raise NotImplementedError

    @abstractmethod
    async def delete_book(self, book_id: int, updated_by_id: int) -> BooksDto:
        raise NotImplementedError


    @abstractmethod
    async def purge_deleted_before(self, cutoff: datetime) -> int:
        raise NotImplementedError