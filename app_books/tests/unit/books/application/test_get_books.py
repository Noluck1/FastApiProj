from collections.abc import Callable
from unittest.mock import MagicMock
import pytest

from app_books.books.application.handlers.books.queries.get_books import GetBooksHandler, GetBooksQuery
from app_books.books.domain.entities.book_entity.book import Book
from shared.dtos.book_list import BookListFilters


@pytest.mark.asyncio
async def test_get_books_returns_paginated_result(
    repository: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    first_book = make_book(book_id=1, title="First book")
    second_book = make_book(book_id=2, title="Second book")

    filters = BookListFilters(
        title_contains="book",
    )

    repository.get_books.return_value = (
        [first_book, second_book], 
        21,
    )

    handler = GetBooksHandler(repository=repository)

    query = GetBooksQuery(
        page=2,
        page_size=20,
        filters=filters,
        sort_by="id",
        sort_order="asc",
    )

    result = await handler.handle(query)

    assert result.item == [first_book, second_book]
    assert result.page == 2
    assert result.page_size == 20
    assert result.total == 21
    assert result.total_pages == 2

    repository.get_books.assert_awaited_once_with(
        page=2,
        page_size=20,
        filters=filters,
        sort_by="id",
        sort_order="asc",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("total", "page_size", "expected_pages"),
    [
        (0, 20, 0),
        (1, 20, 1),
        (20, 20, 1),
        (21, 20, 2),
        (40, 20, 2),
        (41, 20, 3),
    ],
)
async def test_get_books_calculates_total_pages(
    repository: MagicMock,
    total: int,
    page_size: int,
    expected_pages: int,
) -> None:
    repository.get_books.return_value = ([], total)

    handler = GetBooksHandler(repository=repository)

    result = await handler.handle(
        GetBooksQuery(
            page=1,
            page_size=page_size,
            filters=BookListFilters(),
            sort_by="id",
            sort_order="asc",
        )
    )

    assert result.total_pages == expected_pages