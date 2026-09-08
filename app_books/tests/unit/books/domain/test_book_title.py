import pytest

from app_books.books.domain.exceptions import InvalidBookTitleError
from app_books.books.domain.value_objects.book_value_object.book_title import BookTitle

def test_book_title_is_created_from_valid_string() -> None:
    raw_title = "Clean Code"

    title = BookTitle(raw_title)

    assert title.value == "Clean Code"


def test_book_title_removes_outer_spaces() -> None:
    title = BookTitle("   Clean Code   ")

    assert title.value == "Clean Code"

@pytest.mark.parametrize(
    ("raw_title", "expected"),
    [
        ("12345", "12345"),
        ("Clean Code", "Clean Code"),
        ("x" * 100, "x" * 100),
        ("   Clean Code   ", "Clean Code"),
    ],
)
def test_book_title_accepts_valid_values(
    raw_title: str,
    expected: str,
) -> None:
    title = BookTitle(raw_title)

    assert title.value == expected

@pytest.mark.parametrize(
    "raw_title",
    [
        "",
        " ",
        "     ",
        "1234",
        "x" * 101,
    ],
)
def test_book_title_rejects_invalid_values(raw_title: str) -> None:
    with pytest.raises(InvalidBookTitleError):
        BookTitle(raw_title)