from dataclasses import dataclass
from app.shared.application.port.i_handler import IHandler
from app.shared.dtos.favorite_dto import FavoriteDto
from app.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.domain.entities.favorite_entity.favorite_book import FavoriteBook


@dataclass(frozen=True)
class DeleteFavoriteBookCommand:
    book_id: int
    user_id: int


class DeleteFavoriteBookHandler(IHandler[DeleteFavoriteBookCommand, FavoriteBook]):
    def __init__(self, repository: IFavoriteRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: DeleteFavoriteBookCommand) -> FavoriteBook:
        async with self._uow:
            deleted_favorite = await self._repository.delete_favorite_book(
                book_id=request.book_id,
                user_id=request.user_id,
            )

            await self._uow.commit()

            return deleted_favorite
        
        