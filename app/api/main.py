import logging
from fastapi import FastAPI, Request
from dishka.integrations.fastapi import setup_dishka
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.shared.config.database import create_tables, delete_tables, settings
from app.api.routers.book import router as book_router
from app.application.exceptions import NotFoundError
from app.api.dependency_injection.container import build_container
from collections.abc import AsyncIterator
from app.shared.config.logging_config import configure_logging

configure_logging(settings.log_level)

logger = logging.getLogger(__name__)

containter = build_container()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Application startup started")

    await create_tables()
    logger.info("Database tables are ready")

    yield

    logger.info("Application shutdown started")

    await delete_tables()
    await app.state.dishka_container.close()

    logger.info("Application shotdown completed")


app = FastAPI(lifespan=lifespan)

setup_dishka(
    container=containter,
    app=app,
)

app.include_router(book_router)


@app.exception_handler(NotFoundError)
async def not_found_handler(
    request: Request, 
    exc: NotFoundError
) -> JSONResponse:
    logger.warning(
        "Book not found: book_id=%s method=%s path=%s",
        exc.id,
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=404,
        content={"message": f"Книга '{exc.id}' на найдена."}
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled exception: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )