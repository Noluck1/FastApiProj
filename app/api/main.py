import logging
from app.books.bootstrap.scheduler import create_scheduler
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from contextlib import asynccontextmanager
from fastapi.encoders import jsonable_encoder
from app.identity.api.routers.auth import router as auth_router
from app.shared.config.settings import settings
from app.books.api.routers.book import router as book_router
from app.favorite.api.routers.favorite import router as favorite_router
from app.bootstrap.container import build_container
from collections.abc import AsyncIterator
from app.shared.config.logging_config import configure_logging
from app.shared.responses.api_response import error
from app.identity.api.exception_handlers import register_identity_exception_handlers
from app.books.api.exception_handlers import register_books_exception_handlers
from app.favorite.api.exception_handler import register_favorite_exception_handlers
from app.api.exception_handler import register_common_exception_handlers


configure_logging(settings.log_level)

logger = logging.getLogger(__name__)

containter = build_container()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Application startup started")

    scheduler = create_scheduler()
    scheduler.start()

    try:
        yield
    finally:

        scheduler.shutdown(wait=False)
        await app.state.dishka_container.close()

        logger.info("Application shotdown completed")


app = FastAPI(lifespan=lifespan)

register_identity_exception_handlers(app)
register_books_exception_handlers(app)
register_favorite_exception_handlers(app)
register_common_exception_handlers(app)

setup_dishka(
    container=containter,
    app=app,
)
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(favorite_router)


