from shared.application.port.i_unit_of_work import IUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from types import TracebackType

class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._committed = False

    async def __aenter__(self) -> UnitOfWork:
        self._committed = False
        return self

    async def __aexit__(
            self, 
            exc_type: type[BaseException] | None, 
            exc: BaseException | None, 
            tb: TracebackType | None,
    ) -> None:
        
        if exc_type is not None:
            await self.rollback()

        if not self._committed:
            await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()
        self._committed = True

    async def rollback(self) -> None:
        await self._session.rollback()
        self._committed = False