import logging
from dataclasses import dataclass
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.app_books.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.shared.application.port.i_handler import IHandler
from backend.app_books.books.domain.entities.favorite_entity.favorite_book import FavoriteBook

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class AddFavoriteBookCommand:
    book_id: int
    user_id: int

class AddFavoriteBookHandler(IHandler[AddFavoriteBookCommand, FavoriteBook]):
    def __init__(
            self, 
            repository: IFavoriteRepository, 
            book_repository: IBookRepository, 
            uow: IUnitOfWork,
    ):
        self._repository = repository
        self._book_repository = book_repository
        self._uow = uow


    async def handle(self, request: AddFavoriteBookCommand) -> FavoriteBook:
        async with self._uow:
            await self._book_repository.get_book_id(request.book_id)

            favorite = FavoriteBook(
                book_id=request.book_id,
                user_id=request.user_id,
            )

            add_favorite = await self._repository.add_favorite_book(favorite)

            await self._uow.commit()

            logger.info(
                "Favorite: book_id=%s, user_id=%s",
                add_favorite.book_id,
                add_favorite.user_id,
            )

        return add_favorite
        
