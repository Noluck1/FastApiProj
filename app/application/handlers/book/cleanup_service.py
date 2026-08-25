from datetime import datetime, timezone, timedelta
from app.application.repositories.i_book_repository import IBookRepository
from app.application.i_unit_of_work import IUnitOfWork


class BookCleanupService:
    def __init__(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow


    async def purge_expired_books(
        self,
        retention_minutes: int,
    ) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(
            minutes=retention_minutes,
        )

        async with self._uow:
            deleted_count = await self._repository.purge_deleted_before(
                cutoff
            )
            await self._uow.commit()

        return deleted_count