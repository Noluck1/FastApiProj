from dishka import Provider, Scope, provide
from app.application.handlers.book.service import BookService
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_repository import IBookRepository
from app.application.repositories.i_book_access import IBookAccess
from app.application.access.book_access import BookAccess
from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.application.handlers.favorite.favorite_service import FavoriteService

class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def book_access(self) -> IBookAccess:
        return BookAccess()

    @provide
    def book_service(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
        book_access: IBookAccess
    ) -> BookService:
        return BookService(repository=repository, uow=uow, book_access=book_access)

    @provide
    def favorite_service(
        self,
        repository: IFavoriteRepository,
        book_repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> FavoriteService:
        return FavoriteService(repository=repository, book_repository=book_repository, uow=uow)
