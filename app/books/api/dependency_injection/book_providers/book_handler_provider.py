from dishka import Provider, Scope, provide
from app.books.application.ports.book.i_book_repository import IBookRepository
from app.shared.application.port.i_unit_of_work import IUnitOfWork
from app.books.application.handlers.books.command.create_book import CreateBookHandler
from app.books.application.handlers.books.command.delete_book import DeleteBookHandler
from app.books.application.handlers.books.command.put_update_book import PutUppdateBookHandler
from app.books.application.handlers.books.command.patch_update_book import PatchUpdateBookHandler
from app.books.application.handlers.books.queries.get_books import GetBooksHandler
from app.books.application.handlers.books.queries.get_book_id import GetBookIdHandler
from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.books.application.handlers.books.command.cleanup import BookCleanupHandler

class BookHandlerProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def create_book_handler(
        self,
        repository: IBookRepository,
        user_checker: IIdentityCommunication,
        uow: IUnitOfWork,
    ) -> CreateBookHandler:
        return CreateBookHandler(repository=repository, uow=uow, user_checker=user_checker)

    @provide
    def delete_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
        user_checker: IIdentityCommunication,
    ) -> DeleteBookHandler:
        return DeleteBookHandler(reposytory=repository, uow=uow)

    @provide
    def put_update_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
        user_checker: IIdentityCommunication,
    ) -> PutUppdateBookHandler:
        return PutUppdateBookHandler(repository=repository, uow=uow)

    @provide
    def patch_uppdate_book_handler(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
        user_checker: IIdentityCommunication,
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