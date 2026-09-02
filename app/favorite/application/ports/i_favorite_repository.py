from abc import ABC, abstractmethod
from app.shared.dtos.favorite_dto import FavoriteDto
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.book_list import BookListFilters, BookListSortBy, SortOrder


class IFavoriteRepository(ABC):

    @abstractmethod
    async def add_favorite_book(self, book_id: int, user_id: int) -> FavoriteDto:
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

    ) -> tuple[list[BooksDto], int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_favorite_book(self, book_id: int, user_id: int) -> FavoriteDto:
        raise NotImplementedError 