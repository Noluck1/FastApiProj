import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app_books.books.config.settings import books_settings
from app_books.books.application.handlers.books.command.cleanup import BookCleanupCommand, BookCleanupHandler 
from dishka import AsyncContainer, Scope


logger = logging.getLogger(__name__)

async def purge_deleted_books_job(container: AsyncContainer,) -> None:
    async with container(scope=Scope.REQUEST) as request_container:
        handler = await request_container.get(BookCleanupHandler)

        deleted_count = await handler.handle(
            BookCleanupCommand(
                retention_days=books_settings.cleanup_retention_days,
            ),
        )

    logger.info(
        "Expired books physically deleted: count=%s",
        deleted_count,
    )

def create_scheduler(container: AsyncContainer) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    scheduler.add_job(
        purge_deleted_books_job,
        trigger="interval",
        kwargs={"container": container},
        hours=books_settings.cleanup_interval_hours,
        id="purge-deleted-books",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )

    return scheduler