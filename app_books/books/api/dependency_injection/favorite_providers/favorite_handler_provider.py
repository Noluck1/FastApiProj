from dishka import Provider, Scope, provide
from app_books.books.application.ports.book.i_book_repository import IBookRepository
from shared.application.port.i_unit_of_work import IUnitOfWork
from app_books.books.application.handlers.favorite.command.add_favorite import AddFavoriteBookHandler
from app_books.books.application.handlers.favorite.command.delete_favorite import DeleteFavoriteBookHandler
from app_books.books.application.handlers.favorite.queries.get_favorite_books import GetFavoriteBooksHandle
from app_books.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository


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