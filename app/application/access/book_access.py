from app.shared.dtos.auth_dto import UserDto
from app.shared.dtos.book_dto import BooksDto
from app.shared.enums.user_role import UserRole
from app.auth.auth_exceptions import BookAccessDeniedError
from app.application.repositories.i_book_access import IBookAccess


class BookAccess(IBookAccess):

    
    def ensure_can_manage(
        self,
        user: UserDto,
        book: BooksDto,
    ) -> None:
        
        if user.role == UserRole.ADMIN or (user.role == UserRole.AUTHOR and book.author_id == user.id):
            return

        raise BookAccessDeniedError(
            user_id=user.id,
            book_id=book.id,
        )