from app.books.infrastructure.persistence.models.book_model import BooksOrm
from app.books.domain.entities.book import Book
from app.books.domain.value_objects.book_title import BookTitle
from app.books.domain.value_objects.book_description import BookDescription
from app.books.api.dto.book_dto import BooksDto

def book_to_domain(model: BooksOrm) -> Book:
    return Book(
        id=model.id,
        title=BookTitle(model.title),
        description=(
            BookDescription(model.description)
            if model.description is not None
            else None
        ),
        author_id=model.author_id,
        updated_by_id=model.updated_by_id,
        is_deleted=model.is_deleted,
        created_at=model.created_at,
        updated_at=model.updated_at,
        deleted_at=model.deleted_at,
    )

def book_to_orm(book: Book) -> BooksOrm:
    return BooksOrm(
        title=book.title.value,
        description= (
            book.description.value
            if book.description is not None
            else None
        ),
        author_id=book.author_id,
        updated_by_id=book.updated_by_id,
        is_deleted=book.is_deleted,
        deleted_at=book.deleted_at,
    )

def apply_book_to_orm(book: Book, model: BooksOrm) -> None:
    model.title = book.title.value
    model.description = (
        book.description.value
        if book.description is not None
        else None
    )
    model.updated_by_id = book.updated_by_id
    model.is_deleted = book.is_deleted
    model.deleted_at = book.deleted_at


def book_to_dto(book: Book) -> BooksDto:
    return BooksDto(
        id=book.require_id(),
        title=book.title.value,
        description=(
            book.description.value
            if book.description is not None
            else None
        ),
        author_id=book.author_id,
        is_deleted=book.is_deleted,
        created_at=book.created_at,
        updated_at=book.updated_at,
        deleted_at=book.deleted_at,
    )