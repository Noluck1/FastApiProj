from collections.abc import Callable
from unittest.mock import MagicMock
import pytest

from app_books.books.application.exceptions import BookAccessDeniedError
from app_books.books.application.handlers.books.command.put_update_book import PutUpdateBookCommand, PutUpdateBookHandler
from app_books.books.domain.access.book_access_subject import BookAccessSubject
from app_books.books.domain.entities.book_entity.book import Book

@pytest.mark.asyncio
async def test_put_update_book_changes_all_fields(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(
        book_id=10,
        author_id=7,
        title="Old title",
        description="Old description",
    )

    repository.get_book_id.return_value = book

    repository.save.side_effect = lambda saved_book: saved_book

    handler = PutUpdateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = PutUpdateBookCommand(
        book_id=10,
        title="New book title",
        description="New description",
        author=BookAccessSubject(
            user_id=7,
            roles=frozenset({"author"}),
        ),
    )

    result = await handler.handle(command)

    assert result is book
    assert result.title.value == "New book title"
    assert result.description is not None
    assert result.description.value == "New description"
    assert result.updated_by_id == 7

    repository.get_book_id.assert_awaited_once_with(10)
    repository.save.assert_awaited_once_with(book)
    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_put_update_book_denies_another_author(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:

    book = make_book(
        book_id=10,
        author_id=7,
    )

    repository.get_book_id.return_value = book

    handler = PutUpdateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = PutUpdateBookCommand(
        book_id=10,
        title="New book title",
        description=None,
        author=BookAccessSubject(
            user_id=15,
            roles=frozenset({"author"}),
        ),
    )

    

    with pytest.raises(BookAccessDeniedError) as error:
        await handler.handle(command)

    assert error.value.user_id == 15
    assert error.value.book_id == 10

    repository.save.assert_not_awaited()
    uow.commit.assert_not_awaited()

