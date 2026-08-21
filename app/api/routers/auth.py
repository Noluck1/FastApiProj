from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_service import AuthService
from app.shared.dtos.auth_dto import UserDto, RegisterRequest, TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    response_model=UserDto,
    status_code=status.HTTP_201_CREATED,
)
async def register(
        data: RegisterRequest,
        service: FromDishka[AuthService],
) -> UserDto:
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    service: FromDishka[AuthService],
) -> TokenResponse:
    return await service.login(
        username=form.username,
        password=form.password,
    )