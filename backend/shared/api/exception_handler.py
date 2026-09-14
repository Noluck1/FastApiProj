import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from backend.shared.responses.api_response import error
from backend.shared.api.exceptions import ForbiddenError, UnAuthorizedError

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
    _exc: Exception,
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
    request: Request,
    exc: ForbiddenError,
) -> JSONResponse:
    logger.warning(
        "Authorization denied: method=%s path=%s role=%s",
        request.method,
        request.url.path,
        exc.role,
    )

    response = error(message="Insufficient permissions", data={"role": exc.role})
    
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response),
    )

async def un_authorized_error(
    request: Request,
    _exc: UnAuthorizedError,
) -> JSONResponse:
    logger.info(
        "Authentication rejected: method=%s path=%s",
        request.method,
        request.url.path,
    )

    response = error(message="User is not authorized")

    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(response)
    )
