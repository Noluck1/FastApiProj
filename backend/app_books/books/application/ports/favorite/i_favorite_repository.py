from abc import ABC, abstractmethod
from backend.app_books.books.shared.dto.book_list import BookListFilters, BookListSortBy, SortOrder
from backend.app_books.books.domain.entities.favorite_entity.favorite_book import FavoriteBook
from backend.app_books.books.domain.entities.book_entity.book import Book

class IFavoriteRepository(ABC):

    @abstractmethod
    async def add_favorite_book(self, favorite: FavoriteBook) -> FavoriteBook:
        raise NotImplementedError

    @abstractmethod
    async def get_favorite_book(
        self,
        *,
        user_id: int,
        page: int,
        page_size: int,
        filters: BookListFilters,
        sort_by: BookListSortBy,
        sort_order: SortOrder,

    ) -> tuple[list[Book], int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_favorite_book(self, book_id: int, user_id: int) -> FavoriteBook:
        raise NotImplementedError 