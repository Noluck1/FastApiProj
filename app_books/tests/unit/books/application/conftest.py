from collections.abc import Callable
from unittest.mock import MagicMock
import pytest

from app_books.books.application.ports.book.i_book_repository import IBookRepository
from app_books.books.domain.entities.book_entity.book import Book
from app_books.books.domain.value_objects.book_value_object.book_description import BookDescription
from app_books.books.domain.value_objects.book_value_object.book_title import BookTitle
from app_books.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from shared.application.port.i_unit_of_work import IUnitOfWork

@pytest.fixture
def repository() -> MagicMock:
    return MagicMock(spec=IBookRepository)

@pytest.fixture
def favorite_repository() -> MagicMock:
    return MagicMock(spec=IFavoriteRepository)

@pytest.fixture
def uow() -> MagicMock:
    unit_of_work = MagicMock(spec=IUnitOfWork)

    unit_of_work.__aenter__.return_value = unit_of_work
    unit_of_work.__aexit__.return_value = None

    return unit_of_work


@pytest.fixture
def make_book() -> Callable[..., Book]:
    def factory(
        *,
        book_id: int | None = 10,
        author_id: int = 7,
        title: str = "Old title",
        description: str | None = "Old description",
    ) -> Book:
        return Book(
            id=book_id,
            title=BookTitle(title),
            description=(
                BookDescription(description)
                if description is not None
                else None
            ),
            author_id=author_id,
        )
    return factory