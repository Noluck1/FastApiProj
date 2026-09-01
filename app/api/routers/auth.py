from typing import Annotated
from app.shared.responses.api_response import success
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, Form, Cookie, Response
from starlette import status
from app.auth.auth_service import AuthService
from app.shared.dtos.auth_dto import UserDto, RegisterRequest, TokenResponse, LoginRequest
from app.shared.responses.api_response_schema import ApiResponseSchema
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_exceptions import InvalidCredentialsError
from app.api.cookie_manager import set_refresh_cookie
from app.api.mappers.auth_mapper import user_to_dto
from app.auth.dependencies import get_current_user
from app.domain.auth.entities.user import User



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
        service: FromDishka[AuthService],
) -> ApiResponseSchema[UserDto]:

    result = await service.register(data)
    
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
    service: FromDishka[AuthService],
) -> ApiResponseSchema[TokenResponse]:

    result, refresh_token = await service.login(
        username=form.username, 
        password=form.password.get_secret_value(),
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
    service: FromDishka[AuthService],
) -> TokenResponse:

    result, refresh_token = await service.login(
        username=form.username,
        password=form.password,
    )

    set_refresh_cookie(response, refresh_token)
    
    return result

@router.post(
    "/refresh",
    response_model=ApiResponseSchema[TokenResponse],
)
async def refresh(
    response: Response,
    service: FromDishka[AuthService],
    refresh_token: Annotated[
        str | None,
        Cookie(),
    ] = None,
) -> ApiResponseSchema[TokenResponse]:
    if refresh_token is None:
        raise InvalidCredentialsError


    result, new_refresh_token = await service.refresh(
        refresh_token
    )

    set_refresh_cookie(response, new_refresh_token)

    return success(message="Token refreshed", data=result)



@router.post("/logout")
async def logout(
    response: Response,
    service: FromDishka[AuthService],
    refresh_token: Annotated[
        str | None,
        Cookie(),
    ] = None,
) -> ApiResponseSchema[None]:
    if refresh_token is not None:
        await service.logout(refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/auth",
    )

    return success(message="Logged out") 