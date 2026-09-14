from collections.abc import Callable
from unittest.mock import MagicMock
import pytest
from backend.app_books.books.application.exceptions import NotFoundError
from backend.app_books.books.application.handlers.books.queries.get_book_id import GetBookIdHandler, GetBookIdQuery
from backend.app_books.books.domain.entities.book_entity.book import Book


@pytest.mark.asyncio
async def test_get_book_id_returns_book(
    repository: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(book_id=10)

    repository.get_book_id.return_value = book

    handler = GetBookIdHandler(repository=repository)

    result = await handler.handle(
        GetBookIdQuery(book_id=10)
    )

    assert result is book
    repository.get_book_id.assert_awaited_once_with(
        book_id=10,
    )

@pytest.mark.asyncio
async def test_get_book_id_propagates_not_found_error(
    repository: MagicMock,
) -> None:
    repository.get_book_id.side_effect = NotFoundError(id=999)

    handler = GetBookIdHandler(repository=repository)

    with pytest.raises(NotFoundError) as error:
        await handler.handle(
            GetBookIdQuery(book_id=999)
        )

    assert error.value.id == 999