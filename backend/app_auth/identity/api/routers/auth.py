from typing import Annotated
from backend.shared.responses.api_response import success
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, Form, Cookie, Response
from starlette import status
from backend.app_auth.identity.api.dto.auth_dto import (
    UserDto, 
    RegisterRequest, 
    TokenResponse, 
    LoginRequest,
    UpdateFullNameRequest
)
from backend.shared.responses.api_response_schema import ApiResponseSchema
from fastapi.security import OAuth2PasswordRequestForm
from backend.app_auth.identity.application.exceptions import InvalidCredentialsError
from backend.app_auth.identity.api.cookie_manager import set_refresh_cookie
from backend.app_auth.identity.api.auth_mapper import user_to_dto
from backend.app_auth.identity.api.dependencies import get_current_user
from backend.app_auth.identity.domain.entities.user import User
from backend.app_auth.identity.application.handlers.commands.register_user import (
    RegisterUserCommand, 
    RegisterUserHandler
)
from backend.app_auth.identity.application.handlers.commands.login_user import (
    LoginUserHandler, 
    LoginUserCommand
)
from backend.app_auth.identity.application.handlers.commands.refresh_session import (
    RefreshSessionCommand, 
    RefreshSessionHandler
)
from backend.app_auth.identity.application.handlers.commands.logout_user import (
    LogoutUserCommand, 
    LogoutUserHandler
)
from backend.app_auth.identity.application.handlers.commands.update_full_name import (
    UpdateFullNameCommand, 
    UpdateFullNameHandler
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)

@router.post(
    "/register",
    response_model=ApiResponseSchema[UserDto],
    status_code=status.HTTP_201_CREATED,
)
async def register(
        data: Annotated[
            RegisterRequest, 
            Form(),
        ],
        handler: FromDishka[RegisterUserHandler],
) -> ApiResponseSchema[UserDto]:

    result = await handler.handle(
        RegisterUserCommand(
            username=data.username,
            password=data.password.get_secret_value()
        )
    )
    
    return success(message="User registered", data=user_to_dto(result))

@router.get(
    "/me",
    response_model=ApiResponseSchema[UserDto],
)
async def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> ApiResponseSchema[UserDto]:
    return success(
        message="Current user received",
        data=user_to_dto(current_user)
    )

@router.patch(
    "/me/full-name",
    response_model=ApiResponseSchema[UserDto],
)
async def update_my_full_name(
    data: UpdateFullNameRequest,
    handler: FromDishka[UpdateFullNameHandler],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> ApiResponseSchema[UserDto]:
    result = await handler.handle(
        UpdateFullNameCommand(
            user = current_user,
            fields=frozenset(
                data.model_fields_set
            ),
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
        )
    )

    return success(
        message="Full name updated",
        data=user_to_dto(result)
    )


@router.post(
    "/login",
    response_model=ApiResponseSchema[TokenResponse],
)
async def login(
    response: Response,
    form: Annotated[
        LoginRequest,
        Form(),
    ],
    handler: FromDishka[LoginUserHandler],
) -> ApiResponseSchema[TokenResponse]:

    result, refresh_token = await handler.handle(
        LoginUserCommand(
            username=form.username, 
            password=form.password.get_secret_value(),
        )
    )

    set_refresh_cookie(response, refresh_token)

    return success(message="Login successful", data=result)


@router.post(
    "/token",
    response_model=TokenResponse,
    include_in_schema=False
)
async def oauth2_token(
    response: Response,
    form: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    handler: FromDishka[LoginUserHandler],
) -> TokenResponse:

    result, refresh_token = await handler.handle(
        LoginUserCommand(
            username=form.username,
            password=form.password,
        )
    )

    set_refresh_cookie(response, refresh_token)
    
    return result

@router.post(
    "/refresh",
    response_model=ApiResponseSchema[TokenResponse],
)
async def refresh(
    response: Response,
    handler: FromDishka[RefreshSessionHandler],
    refresh_token: Annotated[
        str | None,
        Cookie(),
    ] = None,
) -> ApiResponseSchema[TokenResponse]:
    if refresh_token is None:
        raise InvalidCredentialsError


    result, new_refresh_token = await handler.handle(
        RefreshSessionCommand(
            refresh_token
        )
    )

    set_refresh_cookie(response, new_refresh_token)

    return success(message="Token refreshed", data=result)



@router.post("/logout")
async def logout(
    response: Response,
    handler: FromDishka[LogoutUserHandler],
    refresh_token: Annotated[
        str | None,
        Cookie(),
    ] = None,
) -> ApiResponseSchema[None]:
    if refresh_token is not None:
        await handler.handle(LogoutUserCommand(refresh_token))

    response.delete_cookie(
        key="refresh_token",
        path="/auth",
    )

    return success(message="Logged out") 