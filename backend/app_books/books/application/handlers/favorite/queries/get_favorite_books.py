import logging
from dataclasses import dataclass
from backend.app_books.books.shared.dto.book_list import BookListFilters, BookListSortBy, SortOrder
from backend.shared.application.port.i_handler import IHandler
from backend.app_books.books.api.dto.book.book_dto import BooksDto
from backend.shared.dtos.pagination_dto import PaginatedDto
from backend.app_books.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from backend.app_books.books.domain.entities.book_entity.book import Book

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class GetFavoriteBooksQuery:
    user_id: int
    page: int
    page_size: int
    filters: BookListFilters
    sort_by: BookListSortBy
    sort_order: SortOrder


class GetFavoriteBooksHandle(IHandler[GetFavoriteBooksQuery, PaginatedDto[Book]]):
    def __init__(self, repository: IFavoriteRepository):
        self._repository = repository


    async def handle(self, request: GetFavoriteBooksQuery) -> PaginatedDto[Book]:
        books, total = (
            await self._repository.get_favorite_book(
                user_id=request.user_id,
                page=request.page,
                page_size=request.page_size,
                filters=request.filters,
                sort_by=request.sort_by,
                sort_order=request.sort_order,
            )
        )

        total_pages = (total + request.page_size - 1) // request.page_size

        logger.info(
            "Book favorite: totla=%s",
            total,
        )

        return PaginatedDto[Book](
            item=books,
            page=request.page,
            page_size=request.page_size,
            total=total,
            total_pages=total_pages,
        )
        