import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.shared.responses.api_response import error
from app.favorite.application.exceptions import FavoriteNotFoundError


logger = logging.getLogger(__name__)

def register_favorite_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        FavoriteNotFoundError,
        favorite_not_found_handler,
    )

async def favorite_not_found_handler(
    _request: Request,
    exc: FavoriteNotFoundError,
) -> JSONResponse:
    response = error(
        message="Book is not in favorites",
        data={
            "book_id": exc.book_id,
        },
    )

    return JSONResponse(
        status_code=404,
        content=jsonable_encoder(response)
    )