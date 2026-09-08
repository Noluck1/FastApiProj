import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from shared.responses.api_response import error
from shared.api.exceptions import ForbiddenError, UnAuthorizedError

logger = logging.getLogger(__name__)

def register_common_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        Exception,
        unexpected_error_handler,
    )
    app.add_exception_handler(
        ForbiddenError,
        forbidden_handler,
    )
    app.add_exception_handler(
        UnAuthorizedError,
        un_authorized_error,
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

async def forbidden_handler(
    _request: Request,
    _exc: ForbiddenError,
) -> JSONResponse:

    response = error(message="Insufficient permissions", data={"role": _exc.role})
    
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response),
    )

async def un_authorized_error(
    _request: Request,
    _exc: UnAuthorizedError,
) -> JSONResponse:

    response = error(message="User is not authorized")

    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(response)
    )
