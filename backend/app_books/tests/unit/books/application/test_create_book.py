from unittest.mock import MagicMock
from collections.abc import Callable
import pytest

from backend.app_books.books.application.handlers.books.command.create_book import CreateBookCommand, CreateBookHandler
from backend.app_books.books.domain.entities.book_entity.book import Book

@pytest.mark.asyncio
async def test_create_book_returns_created_book(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:

    created_book = make_book(
        book_id=42,
        title="Clean Code",
        description=None,
        author_id=7,
    )

    repository.add_book.return_value = created_book

    handler = CreateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = CreateBookCommand(
        title="Clean Code",
        description=None,
        author_id=7,
    )

    result = await handler.handle(command)

    assert result is created_book
    assert result.id == 42
    assert result.title.value == "Clean Code"
    assert result.author_id == 7

@pytest.mark.asyncio
async def test_create_book_passes_new_book_to_repository(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:

    repository.add_book.return_value = make_book(
        book_id=42,
        title="Clean Code",
        description=None,
        author_id=7,
    )

    handler = CreateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = CreateBookCommand(
        title="Clean Code",
        description=None,
        author_id=7,
    )

    await handler.handle(command)

    repository.add_book.assert_awaited_once()

    passed_book = repository.add_book.await_args.args[0]

    assert isinstance(passed_book, Book)
    assert passed_book.id is None
    assert passed_book.title.value == "Clean Code"
    assert passed_book.description is None
    assert passed_book.author_id == 7

@pytest.mark.asyncio
async def test_create_book_commits_transaction(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:

    repository.add_book.return_value = make_book(
        book_id=42,
        title="Clean Code",
        description=None,
        author_id=7,
    )

    handler = CreateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = CreateBookCommand(
        title="Clean Code",
        description=None,
        author_id=7,
    )

    await handler.handle(command)

    uow.commit.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_create_book_does_not_commit_when_repository_fails(
    repository: MagicMock,
    uow: MagicMock,
) -> None:

    repository.add_book.side_effect = RuntimeError(
        "Database is unavailable",
    )

    handler = CreateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = CreateBookCommand(
        title="Clean Code",
        description=None,
        author_id=7,
    )

    with pytest.raises(
        RuntimeError, 
        match="Database is unavailable",
    ):
        await handler.handle(command)

    uow.commit.assert_not_awaited()