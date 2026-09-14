from datetime import datetime, timezone
import pytest

from backend.app_books.books.domain.entities.book_entity.book import Book
from backend.app_books.books.domain.exceptions import BookAlreadyDeletedError
from backend.app_books.books.domain.value_objects.book_value_object.book_title import BookTitle

def make_book(book_id: int | None = 10) -> Book:
    return Book(
        id=book_id,
        title=BookTitle("Clean Code"),
        description=None,
        author_id=7,
    )

def test_require_id_returns_book_id() -> None:
    book = make_book(book_id=10)
    result = book.require_id()
    assert result == 10


def test_require_id_raises_when_book_has_no_id() -> None:
    book = make_book(book_id=None)

    with pytest.raises(
        RuntimeError,
        match="Persisted book must have an id",
    ):
        book.require_id()

def test_change_title_changes_title_and_updated_by() -> None:
    book = make_book()

    new_title = BookTitle("Domain Driver Design")

    book.change_title(
        title=new_title,
        updated_by_id=15,
    )

    assert book.title == new_title
    assert book.updated_by_id == 15

def test_delete_marks_book_as_deleted() -> None:
    book = make_book()
    deleted_at = datetime(
        2026,
        9,
        4,
        12,
        0,
        tzinfo=timezone.utc,
    )

    book.delete(
        updated_by_id=7,
        deleted_at=deleted_at,
    )

    assert book.is_deleted is True
    assert book.deleted_at == deleted_at
    assert book.updated_by_id == 7

def test_delete_raises_when_book_already_deleted() -> None:
    book = make_book()
    deleted_at = datetime(
        2026,
        9,
        4,
        12,
        0,
        tzinfo=timezone.utc,
    )

    book.delete(
        updated_by_id=7,
        deleted_at=deleted_at,
    )

    with pytest.raises(BookAlreadyDeletedError):
        book.delete(
            updated_by_id=7,
            deleted_at=deleted_at,
        )