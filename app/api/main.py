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
    UnAuthorizedError,
    BookAccessDeniedError,
)
from fastapi.encoders import jsonable_encoder
from app.api.routers.auth import router as auth_router
from app.shared.config.settings import settings
from app.api.routers.book import router as book_router
from app.application.exceptions import NotFoundError
from app.api.dependency_injection.container import build_container
from collections.abc import AsyncIterator
from app.shared.config.logging_config import configure_logging
from app.shared.responses.api_response import error

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

    response = error(message=f"Book not found", data={"book_id": exc.id})

    return JSONResponse(
        status_code=404,
        content=jsonable_encoder(response)
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    _request: Request,
    _exc: InvalidCredentialsError,
) -> JSONResponse:

    response = error(message="Invalid username, password or token")
    
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(response),
        headers={"WWW-Authenticate": "Bearer"}
    )


@app.exception_handler(InactiveUserError)
async def inactive_user_handler(
    _request: Request,
    _exc: InactiveUserError,
) -> JSONResponse:

    response = error(message="User is inactive")
    
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response),
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(
    _request: Request,
    _exc: ForbiddenError,
) -> JSONResponse:

    response = error(message="Insufficient permissions", data={"role": _exc.role})
    
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response),
    )


@app.exception_handler(UsernameAlreadyExistsError)
async def username_exists_handler(
    _request: Request,
    exc: UsernameAlreadyExistsError,
) -> JSONResponse:

    response = error(message="Username already exists", data={"field": exc.username})
    
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder(response),
    )

@app.exception_handler(UnAuthorizedError)
async def un_authorized_error(
    _request: Request,
    _exc: UnAuthorizedError,
) -> JSONResponse:

    response = error(message="User is not authorized")

    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(response)
    )

@app.exception_handler(BookAccessDeniedError)
async def not_book_owner_error(
    _request: Request,
    exc: BookAccessDeniedError,
) -> JSONResponse:

    response = error(
        message="This book does not belong to the current user", 
        data={
            "book_id": exc.book_id,
            "user_id": exc.user_id,
        },
    )

    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response)
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

    response = error(message="Internal server error")

    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(response)
    )
