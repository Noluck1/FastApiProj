from collections.abc import Callable
from unittest.mock import MagicMock
import pytest
from app_books.books.application.handlers.books.command.delete_book import DeleteBookHandler, DeleteBookCommand
from app_books.books.domain.access.book_access_subject import BookAccessSubject
from app_books.books.domain.entities.book_entity.book import Book

@pytest.mark.asyncio
async def test_delete_book_marks_book_as_deleted(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(
        book_id=10,
        author_id=7,
    )

    repository.get_book_id.return_value = book
    repository.save.side_effect = lambda saved_book: saved_book

    handler = DeleteBookHandler(
        repository=repository,
        uow=uow,
    )

    command = DeleteBookCommand(
        book_id=10,
        author=BookAccessSubject(
            user_id=7,
            roles=frozenset({"author"}),
        ),
    )

    result = await handler.handle(command)

    assert result is book
    assert result.is_deleted is True
    assert result.deleted_at is not None
    assert result.deleted_at.tzinfo is not None
    assert result.updated_by_id == 7

    repository.get_book_id.assert_awaited_once_with(10)
    repository.save.assert_awaited_once_with(book)
    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_admin_can_delete_another_users_book(
    repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(
        book_id=10,
        author_id=99,
    )

    repository.get_book_id.return_value = book
    repository.save.side_effect = lambda saved_book: saved_book

    handler = DeleteBookHandler(
        repository=repository,
        uow=uow,
    )

    result = await handler.handle(
        DeleteBookCommand(
            book_id=10,
            author=BookAccessSubject(
                user_id=7,
                roles=frozenset({"admin"}),
            ),
        )
    )

    assert result.is_deleted is True
    assert result.updated_by_id == 7
    uow.commit.assert_awaited_once_with()
    