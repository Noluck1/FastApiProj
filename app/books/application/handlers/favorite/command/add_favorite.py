from dataclasses import dataclass
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.shared.application.port.i_handler import IHandler
from app.books.domain.entities.favorite_entity.favorite_book import FavoriteBook
from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.books.application.exceptions import ReferencedUserNotFoundError


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
            user_checker: IIdentityCommunication
    ):
        self._repository = repository
        self._book_repository = book_repository
        self._uow = uow
        self._user_checker = user_checker


    async def handle(self, request: AddFavoriteBookCommand) -> FavoriteBook:
        async with self._uow:
            await self._book_repository.get_book_id(request.book_id)

            user_exists = await self._user_checker.get(request.user_id)

            if not user_exists:
                raise ReferencedUserNotFoundError(user_id=request.user_id)

            favorite = FavoriteBook(
                book_id=request.book_id,
                user_id=request.user_id,
            )

            add_favorite = await self._repository.add_favorite_book(favorite)

            await self._uow.commit()

        return add_favorite
        
