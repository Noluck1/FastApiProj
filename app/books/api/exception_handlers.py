import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.shared.responses.api_response import error
from app.books.application.exceptions import NotFoundError, BookAccessDeniedError

logger = logging.getLogger(__name__)

def register_books_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        NotFoundError,
        not_found_handler,
    )
    app.add_exception_handler(
        BookAccessDeniedError,
        not_book_owner_error,
    )


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