from collections.abc import Callable
from unittest.mock import MagicMock
import pytest
from app_books.books.application.handlers.books.command.patch_update_book import PatchUpdateBookCommand, PatchUpdateBookHandler
from app_books.books.domain.access.book_access_subject import BookAccessSubject
from app_books.books.domain.entities.book_entity.book import Book
from app_books.books.domain.exceptions import InvalidBookTitleError

@pytest.mark.asyncio
async def test_pach_changes_only_title(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(
        title="Old title",
        description="Old description",
    )

    repository.get_book_id.return_value = book
    repository.save.side_effect = lambda saved_book: saved_book

    handler = PatchUpdateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = PatchUpdateBookCommand(
        book_id=10,
        title="New book title",
        description=None,
        changed_fields=frozenset({"title"}),
        author=BookAccessSubject(
            user_id=7,
            roles=frozenset({"author"}),
        ),
    )

    result = await handler.handle(command)

    assert result.title.value == "New book title"
    assert result.description is not None
    assert result.description.value == "Old description"

    repository.save.assert_awaited_once_with(book)
    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_patch_can_explicitly_clear_description(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(
        description="Old description",
    )

    repository.get_book_id.return_value = book
    repository.save.side_effect = lambda saved_book: saved_book

    handler = PatchUpdateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = PatchUpdateBookCommand(
        book_id=10,
        title=None,
        description=None,
        changed_fields=frozenset({"description"}),
        author=BookAccessSubject(
            user_id=7,
            roles=frozenset({"author"}),
        ),
    )

    result = await handler.handle(command)

    assert result.title.value == "Old title"
    assert result.description is None
    assert result.updated_by_id == 7

    repository.save.assert_awaited_once_with(book)
    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_patch_rejects_null_title(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book()
    repository.get_book_id.return_value = book


    handler = PatchUpdateBookHandler(
        repository=repository,
        uow=uow,
    )

    command = PatchUpdateBookCommand(
        book_id=10,
        title=None,
        description=None,
        changed_fields=frozenset({"title"}),
        author=BookAccessSubject(
            user_id=7,
            roles=frozenset({"author"}),
        ),
    )

    with pytest.raises(InvalidBookTitleError):
        await handler.handle(command)

    repository.save.assert_not_awaited()
    uow.commit.assert_not_awaited()