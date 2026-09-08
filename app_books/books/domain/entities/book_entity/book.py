from dataclasses import dataclass
from datetime import datetime
from app_books.books.domain.value_objects.book_value_object.book_title import BookTitle
from app_books.books.domain.value_objects.book_value_object.book_description import BookDescription
from app_books.books.domain.exceptions import BookAlreadyDeletedError


@dataclass(slots=True)
class Book:
    id: int | None
    title: BookTitle
    description: BookDescription | None
    author_id: int

    updated_by_id: int | None = None
    is_deleted: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def require_id(self) -> int:
        if self.id is None:
            raise RuntimeError("Persisted book must have an id")

        return self.id

    def change_title(
        self,
        title: BookTitle,
        updated_by_id: int,
    ) -> None:
        self.title = title
        self.updated_by_id = updated_by_id

    def change_description(
        self,
        description: BookDescription | None,
        updated_by_id: int,
    ) -> None:
        self.description = description
        self.updated_by_id = updated_by_id

    def delete(
        self,
        updated_by_id: int,
        deleted_at: datetime,
    ) -> None:
        if self.is_deleted:
            raise BookAlreadyDeletedError

        self.is_deleted = True
        self.deleted_at = deleted_at
        self.updated_by_id = updated_by_id