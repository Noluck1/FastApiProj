from dishka import Provider, Scope, provide
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.application.handlers.command.create_book import CreateBookHandler
from app.books.application.handlers.command.delete_book import DeleteBookHandler
from app.books.application.handlers.command.put_update_book import PutUppdateBookHandler
from app.books.application.handlers.command.patch_update_book import PatchUpdateBookHandler
from app.books.application.handlers.queries.get_books import GetBooksHandler
from app.books.application.handlers.queries.get_book_id import GetBookIdHandler

class BookHandlerProvider(Provider):
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