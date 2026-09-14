from unittest.mock import MagicMock
import pytest

from backend.app_books.books.application.exceptions import FavoriteNotFoundError
from backend.app_books.books.application.handlers.favorite.command.delete_favorite import (
    DeleteFavoriteBookCommand, 
    DeleteFavoriteBookHandler
)
from backend.app_books.books.domain.entities.favorite_entity.favorite_book import FavoriteBook


@pytest.mark.asyncio
async def test_delete_favorite_returns_deleted_favorite(
    favorite_repository: MagicMock,
    uow: MagicMock,
) -> None:
    deleted_favorite = FavoriteBook(
        user_id=7,
        book_id=10,
    )

    favorite_repository.delete_favorite_book.return_value = (
        deleted_favorite
    )

    handler = DeleteFavoriteBookHandler(
        repository=favorite_repository,
        uow=uow,
    )

    result = await handler.handle(
        DeleteFavoriteBookCommand(
            book_id=10,
            user_id=7,
        )
    )

    assert result is deleted_favorite

    favorite_repository.delete_favorite_book.assert_awaited_once_with(
        book_id=10,
        user_id=7,
    )

    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_delete_favorite_does_not_commit_when_missing(
    favorite_repository: MagicMock,
    uow: MagicMock,
) -> None:
    favorite_repository.delete_favorite_book.side_effect = (
        FavoriteNotFoundError(
            user_id=7,
            book_id=10,
        )
    )

    handler = DeleteFavoriteBookHandler(
        repository=favorite_repository,
        uow=uow,
    )

    with pytest.raises(FavoriteNotFoundError) as error:
        await handler.handle(
            DeleteFavoriteBookCommand(
                book_id=10,
                user_id=7,
            )
        )

    assert error.value.user_id == 7
    assert error.value.book_id == 10
    uow.commit.assert_not_awaited()