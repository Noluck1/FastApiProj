import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.app_books.books.api.dependency_injection.container import build_books_container
from backend.app_books.books.api.setup import register_books_api
from backend.app_books.books.bootstrap.scheduler import create_scheduler
from backend.app_books.books.config.settings import books_settings
from backend.app_books.books.infrastructure.persistence.database import books_engine
from backend.shared.api.exception_handler import register_common_exception_handlers
from backend.shared.config.logging_config import configure_logging

configure_logging(books_settings.log_level)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    container = build_books_container()

    @asynccontextmanager
    async def lifespan(
        _app: FastAPI,
    ) -> AsyncIterator[None]:
        scheduler = create_scheduler(container)

        try:
            scheduler.start()
            logger.info("Books service started")

            yield

        finally:
            if scheduler.running:
                scheduler.shutdown(wait=False)

            await container.close()
            await books_engine.dispose()

            logger.info("Books service stopped")

    application = FastAPI(
        title="Books service",
        lifespan=lifespan,
    )

    setup_dishka(
        container=container,
        app=application,
    )

    register_common_exception_handlers(application)
    register_books_api(application)

    return application

app = create_app()