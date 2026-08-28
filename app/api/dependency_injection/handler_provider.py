from dishka import Provider, Scope, provide
from app.application.repositories.i_book_repository import IBookRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.application.handlers.book.command.create_book import CreateBookHandler
from app.application.handlers.book.command.delete_book import DeleteBookHandler
from app.application.handlers.book.command.put_update_book import PutUppdateBookHandler
from app.application.handlers.book.command.patch_update_book import PatchUpdateBookHandler
from app.application.handlers.book.queries.get_books import GetBooksHandler
from app.application.handlers.book.queries.get_book_id import GetBookIdHandler
from app.application.handlers.favorite.command.add_favorite import AddFavoriteBookHandler
from app.application.handlers.favorite.command.delete_favorite import DeleteFavoriteBookHandler
from app.application.handlers.favorite.queries.get_favorite_books import GetFavoriteBooksHandle
from app.application.repositories.i_favorite_repository import IFavoriteRepository



class HandlerProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def create_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> CreateBookHandler:
        return CreateBookHandler(repository=repository, uow=uow)

    @provide
    def delete_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> DeleteBookHandler:
        return DeleteBookHandler(reposytory=repository, uow=uow)

    @provide
    def put_update_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> PutUppdateBookHandler:
        return PutUppdateBookHandler(repository=repository, uow=uow)

    @provide
    def patch_uppdate_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> PatchUpdateBookHandler:
        return PatchUpdateBookHandler(repository=repository, uow=uow)

    @provide
    def get_books_handler(
        self,
        repository: IBookRepository,
    ) -> GetBooksHandler:
        return GetBooksHandler(repository=repository)

    @provide
    def get_book_id_handler(
        self,
        repository: IBookRepository,
    ) -> GetBookIdHandler:
        return GetBookIdHandler(repository=repository)

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