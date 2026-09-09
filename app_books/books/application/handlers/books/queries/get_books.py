import logging
from dataclasses import dataclass
from app_books.books.shared.dto.book_list import BookListFilters, BookListSortBy, SortOrder
from shared.application.port.i_handler import IHandler
from shared.dtos.pagination_dto import PaginatedDto
from app_books.books.application.ports.book.i_book_repository import IBookRepository
from app_books.books.domain.entities.book_entity.book import Book

logger  = logging.getLogger(__name__)

@dataclass(frozen=True)
class GetBooksQuery:
    page: int
    page_size: int
    filters: BookListFilters
    sort_by: BookListSortBy
    sort_order: SortOrder


class GetBooksHandler(IHandler[GetBooksQuery, PaginatedDto[Book]]):
    def __init__(self, repository: IBookRepository):
        self._repository = repository


    async def handle(self, request: GetBooksQuery) -> PaginatedDto[Book]:
        books, total = await self._repository.get_books(
            page=request.page,
            page_size=request.page_size,
            filters=request.filters,
            sort_by=request.sort_by,
            sort_order=request.sort_order,
        )

        total_pages = (total + request.page_size - 1) // request.page_size

        logger.debug(
            "Books retrieved: page=%s page_size=%s "
            "result_count=%s total=%s",
            request.page,
            request.page_size,
            len(books),
            total,
        )

        return PaginatedDto[Book](
            item=books,
            page=request.page,
            page_size=request.page_size,
            total=total,
            total_pages=total_pages
        )