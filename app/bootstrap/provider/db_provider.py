from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.shared.infrastructure.persistence.sqlalchemy.database import new_session
from collections.abc import AsyncIterable

class DbProvider(Provider):
    @provide(scope=Scope.APP)
    def session_factory(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with factory() as session:
                yield session
            

            

