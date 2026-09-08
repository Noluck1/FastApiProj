from app_books.books.application.exceptions import BookAccessDeniedError
from app_books.books.domain.access.book_access_subject import BookAccessSubject
from app_books.books.domain.entities.book_entity.book import Book

def ensure_can_manage(author: BookAccessSubject, book: Book) -> None:

    is_admin = author.has_role("admin")

    is_author_owner = (
        author.has_role("author")
        and book.author_id == author.user_id
    )

    if is_admin or is_author_owner:
        return

    raise BookAccessDeniedError(
        user_id=author.user_id,
        book_id=book.require_id(),
    )