import logging
from fastapi import FastAPI, Request
from dishka.integrations.fastapi import setup_dishka
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.auth.auth_exceptions import (
    ForbiddenError,
    InactiveUserError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)
from app.api.routers import auth as auth_router
from app.shared.config.database import settings
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

    yield

    logger.info("Application shutdown started")

    await app.state.dishka_container.close()

    logger.info("Application shotdown completed")


app = FastAPI(lifespan=lifespan)

setup_dishka(
    container=containter,
    app=app,
)
app.include_router(auth_router)
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


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": "Invalid username, password or token"},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(InactiveUserError)
async def inactive_user_handler(
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"message": "User is inactive"},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"message": "Insufficient permissions"},
    )


@app.exception_handler(UsernameAlreadyExistsError)
async def username_exists_handler(
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"message": "Username already exists"},
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