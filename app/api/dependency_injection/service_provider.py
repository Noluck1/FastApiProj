from dishka import Provider, Scope, provide
from app.application.handlers.book.service import BookService
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_repository import IBookRepository


class ServiceProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def book_service(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> BookService:
        return BookService(repository=repository, uow=uow)
