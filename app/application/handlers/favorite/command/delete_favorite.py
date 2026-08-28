from dataclasses import dataclass
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.favorite_dto import FavoriteDto
from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.shared.dtos.auth_dto import UserDto


@dataclass(frozen=True)
class DeleteFavoriteBookCommand:
    book_id: int
    current_user: UserDto


class DeleteFavoriteBookHandler(IHandler[DeleteFavoriteBookCommand, FavoriteDto]):
    def __init__(self, repository: IFavoriteRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: DeleteFavoriteBookCommand) -> FavoriteDto:
        async with self._uow:
            deleted_favorite = await self._repository.delete_favorite_book(
                book_id=request.book_id,
                user_id=request.current_user.id
            )

            await self._uow.commit()

            return deleted_favorite
        
        