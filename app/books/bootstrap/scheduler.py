import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.shared.infrastructure.persistence.sqlalchemy.database import  new_session
from app.shared.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork
from app.books.infrastructure.persistence.repositories.book.book_repository import BookRepository
from app.shared.config.settings import settings
from app.books.application.handlers.books.command.cleanup import BookCleanupCommand, BookCleanupHandler 


logger = logging.getLogger(__name__)




async def purge_deleted_books_job() -> None:
    async with new_session() as session:
        handler = BookCleanupHandler(
            repository=BookRepository(session),
            uow=UnitOfWork(session),
        )

        deleted_count = await handler.handle(
            BookCleanupCommand(
                retention_days=settings.book_cleanup_retention_days,
            ),
        )

    logger.info(
        "Expired books physically deleted: count=%s",
        deleted_count,
    )

def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    scheduler.add_job(
        purge_deleted_books_job,
        trigger="interval",
        hours=settings.book_cleanup_interval_hours,
        id="purge-deleted-books",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )

    return scheduler