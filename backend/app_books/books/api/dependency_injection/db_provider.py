from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app_books.books.infrastructure.persistence.database import (
    books_session_factory,
)
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.shared.infrastructure.persistence.sqlalchemy.unit_of_work import (
    UnitOfWork,
)


class BooksDbProvider(Provider):
    @provide(scope=Scope.APP)
    def session_factory(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        return books_session_factory

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def unit_of_work(
        self,
        session: AsyncSession,
    ) -> IUnitOfWork:
        return UnitOfWork(session)