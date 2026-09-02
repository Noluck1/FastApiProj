import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.shared.responses.api_response import error


logger = logging.getLogger(__name__)

def register_common_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        Exception,
        unexpected_error_handler,
    )


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