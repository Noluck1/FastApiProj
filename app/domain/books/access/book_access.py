from app.domain.auth.entities.user import User
from app.domain.auth.enums.user_role import UserRole
from app.shared.dtos.book_dto import BooksDto
from app.auth.auth_exceptions import BookAccessDeniedError


def ensure_can_manage(user: User, book: BooksDto) -> None:
            
    if user.role == UserRole.ADMIN or (user.role == UserRole.AUTHOR and book.author_id == user.id):
        return

    raise BookAccessDeniedError(
        user_id=user.id,
        book_id=book.id,
    )