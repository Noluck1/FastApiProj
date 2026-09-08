from collections.abc import Callable
from unittest.mock import MagicMock
import pytest
from app_books.books.application.exceptions import (
    FavoriteAlreadyExistsError, 
    NotFoundError, 
)
from app_books.books.application.handlers.favorite.command.add_favorite import (
    AddFavoriteBookCommand, 
    AddFavoriteBookHandler
)
from app_books.books.domain.entities.book_entity.book import Book
from app_books.books.domain.entities.favorite_entity.favorite_book import FavoriteBook

@pytest.mark.asyncio
async def test_add_favorite_returns_created_favorite(
    repository: MagicMock,
    uow: MagicMock,
    favorite_repository: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    book = make_book(book_id=10)

    repository.get_book_id.return_value = book

    create_favorite = FavoriteBook(
        user_id=7,
        book_id=10,
    )

    favorite_repository.add_favorite_book.return_value = (
        create_favorite
    )

    handler = AddFavoriteBookHandler(
        repository=favorite_repository,
        book_repository=repository,
        uow=uow,
    )

    command = AddFavoriteBookCommand(
        book_id=10,
        user_id=7,
    )

    result = await handler.handle(command)

    assert result is create_favorite
    assert result.user_id == 7
    assert result.book_id == 10


@pytest.mark.asyncio
async def test_add_favorite_cheks_book_and_user(
    repository: MagicMock,
    favorite_repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    
    repository.get_book_id.return_value = make_book(
        book_id=10,
    )

    favorite_repository.add_favorite_book.return_value = (
        FavoriteBook(user_id=7, book_id=10)
    )

    handler = AddFavoriteBookHandler(
        repository=favorite_repository,
        book_repository=repository,
        uow=uow,
    )

    await handler.handle(
        AddFavoriteBookCommand(
            book_id=10,
            user_id=7,
        )
    )

    repository.get_book_id.assert_awaited_once_with(10)

    favorite_repository.add_favorite_book.assert_awaited_once_with(
        FavoriteBook(
            user_id=7,
            book_id=10,
        )
    )

    uow.commit.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_add_favorite_does_not_continue_when_book_missing(
    repository: MagicMock,
    favorite_repository: MagicMock,
    uow: MagicMock,
) -> None:
    repository.get_book_id.side_effect = NotFoundError(id=10)

    handler = AddFavoriteBookHandler(
        repository=favorite_repository,
        book_repository=repository,
        uow=uow,
    )

    with pytest.raises(NotFoundError) as error:
        await handler.handle(
            AddFavoriteBookCommand(
                book_id=10,
                user_id=7,
            )
        )

    assert error.value.id == 10

    favorite_repository.add_favorite_book.assert_not_awaited()
    uow.commit.assert_not_awaited()

@pytest.mark.asyncio
async def test_add_favorite_does_not_commit_duplicate(
    repository: MagicMock,
    favorite_repository: MagicMock,
    uow: MagicMock,
    make_book: Callable[..., Book],
) -> None:
    
    repository.get_book_id.return_value = make_book(
        book_id=10,
    )

    favorite_repository.add_favorite_book.side_effect = (
        FavoriteAlreadyExistsError(
            user_id=7,
            book_id=10,
        )
    )

    handler = AddFavoriteBookHandler(
        repository=favorite_repository,
        book_repository=repository,
        uow=uow,
    )

    with pytest.raises(FavoriteAlreadyExistsError) as error:
        await handler.handle(
            AddFavoriteBookCommand(
                book_id=10,
                user_id=7,
            )
        )

    assert error.value.user_id == 7
    assert error.value.book_id == 10
    uow.commit.assert_not_awaited()