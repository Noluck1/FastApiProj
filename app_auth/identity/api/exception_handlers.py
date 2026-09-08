from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app_auth.identity.application.exceptions import InvalidCredentialsError, UsernameAlreadyExistsError
from app_auth.identity.domain.exceptions import InactiveUserError
from shared.responses.api_response import error
from fastapi.encoders import jsonable_encoder


def register_identity_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        InvalidCredentialsError,
        invalid_credentials_handler,
    )
    app.add_exception_handler(
        UsernameAlreadyExistsError,
        username_exists_handler,
    )
    app.add_exception_handler(
        InactiveUserError,
        inactive_user_handler,
    )


async def username_exists_handler(
    _request: Request,
    exc: UsernameAlreadyExistsError,
) -> JSONResponse:

    response = error(message="Username already exists", data={"field": exc.username})
    
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder(response),
    )

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

async def inactive_user_handler(
    _request: Request,
    _exc: InactiveUserError,
) -> JSONResponse:

    response = error(message="User is inactive")
    
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder(response),
    )
