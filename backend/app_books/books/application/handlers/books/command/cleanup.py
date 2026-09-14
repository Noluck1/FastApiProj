from dataclasses import dataclass
from backend.shared.application.port.i_handler import IHandler
from backend.app_books.books.application.ports.book.i_book_repository import IBookRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from datetime import datetime, timedelta, timezone

@dataclass(frozen=True)
class BookCleanupCommand:
    retention_days: int


class BookCleanupHandler(IHandler[BookCleanupCommand, int]):
    def __init__(self, repository: IBookRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: BookCleanupCommand) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(
            days=request.retention_days,
        )

        async with self._uow:
            deleted_count = await self._repository.purge_deleted_before(
                cutoff 
            )
            await self._uow.commit()

        return deleted_count