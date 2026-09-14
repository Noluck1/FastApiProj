import logging
from time import perf_counter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.app_books.books.config.settings import books_settings
from backend.app_books.books.application.handlers.books.command.cleanup import BookCleanupCommand, BookCleanupHandler 
from dishka import AsyncContainer, Scope


logger = logging.getLogger(__name__)

async def purge_deleted_books_job(container: AsyncContainer,) -> None:
    started_at = perf_counter()

    logger.info(
        "Cleanup job started: job_id=purge-deleted-books "
        "retention_days=%s",
        books_settings.cleanup_retention_days,
    )
    try:
        async with container(
            scope=Scope.REQUEST
        ) as request_container:
            handler = await request_container.get(
                BookCleanupHandler
            )

            deleted_count = await handler.handle(
                BookCleanupCommand(
                    retention_days=books_settings.cleanup_retention_days,
                ),
            )
    except Exception:
        logger.exception(
            "Cleanuo job failed: job_id=purge-deleted-books "
            "duration_ms=%.2f",
            (perf_counter() - started_at) * 1000,
        )
        raise

    logger.info(
        "Cleanup job completed: job_id=purge-deleted-books "
        "deleted_count=%s duration_ms=%.2f",
        deleted_count,
        (perf_counter() - started_at) * 1000,
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