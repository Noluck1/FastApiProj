from dataclasses import dataclass
from app.application.repositories.i_book_repository import IBookRepository
from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.favorite_dto import FavoriteDto
from app.domain.auth.entities.user import User


@dataclass(frozen=True)
class AddFavoriteBookCommand:
    book_id: int
    current_user: User

class AddFavoriteBookHandler(IHandler[AddFavoriteBookCommand, FavoriteDto]):
    def __init__(
            self, 
            repository: IFavoriteRepository, 
            book_repository: IBookRepository, 
            uow: IUnitOfWork
    ):
        self._repository = repository
        self._book_repository = book_repository
        self._uow = uow


    async def handle(self, request: AddFavoriteBookCommand) -> FavoriteDto:
        user_id = request.current_user.require_id()

        async with self._uow:

            await self._book_repository.get_book_id(request.book_id)

            add_favorite = await self._repository.add_favorite_book(
                book_id=request.book_id,
                user_id=user_id,
            )

            await self._uow.commit()

        return add_favorite
        
