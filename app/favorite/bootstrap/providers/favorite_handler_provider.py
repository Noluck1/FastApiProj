from dishka import Provider, Scope, provide
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.favorite.application.handlers.command.add_favorite import AddFavoriteBookHandler
from app.favorite.application.handlers.command.delete_favorite import DeleteFavoriteBookHandler
from app.favorite.application.handlers.queries.get_favorite_books import GetFavoriteBooksHandle
from app.favorite.application.ports.i_favorite_repository import IFavoriteRepository

class FavoriteHandlerProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def add_book_favorite_handler(
        self,
        repository: IFavoriteRepository,
        book_repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> AddFavoriteBookHandler:
        return AddFavoriteBookHandler(repository=repository, book_repository=book_repository, uow=uow)

    @provide
    def delete_favorite_book_handler(
        self,
        reposytory: IFavoriteRepository,
        uow: IUnitOfWork,
    ) -> DeleteFavoriteBookHandler:
        return DeleteFavoriteBookHandler(repository=reposytory, uow=uow)

    @provide
    def get_favorite_books_handler(
        self,
        repository: IFavoriteRepository,
    ) -> GetFavoriteBooksHandle:
        return GetFavoriteBooksHandle(repository=repository)