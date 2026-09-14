from dishka import Provider, Scope, provide
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_books.books.application.handlers.books.command.create_book import CreateBookHandler
from backend.app_books.books.application.handlers.books.command.delete_book import DeleteBookHandler
from backend.app_books.books.application.handlers.books.command.put_update_book import PutUpdateBookHandler
from backend.app_books.books.application.handlers.books.command.patch_update_book import PatchUpdateBookHandler
from backend.app_books.books.application.handlers.books.queries.get_books import GetBooksHandler
from backend.app_books.books.application.handlers.books.queries.get_book_id import GetBookIdHandler
from backend.app_books.books.application.handlers.books.command.cleanup import BookCleanupHandler

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
        return DeleteBookHandler(repository=repository, uow=uow)

    @provide
    def put_update_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> PutUpdateBookHandler:
        return PutUpdateBookHandler(repository=repository, uow=uow)

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
    def cleanup_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> BookCleanupHandler:
        return BookCleanupHandler(
            repository=repository,
            uow=uow,
        )