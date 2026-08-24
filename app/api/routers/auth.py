from typing import Annotated
from app.shared.responses.api_response import success
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, Form
from starlette import status
from app.auth.auth_service import AuthService
from app.shared.dtos.auth_dto import UserDto, RegisterRequest, TokenResponse, LoginRequest
from app.shared.responses.api_response_schema import ApiResponseSchema

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
    
    return success(message="User registered", data=result)


@router.post(
    "/login",
    response_model=ApiResponseSchema[TokenResponse],
)
async def login(
    form: Annotated[
        LoginRequest,
        Form(),
    ],
    service: FromDishka[AuthService],
) -> ApiResponseSchema[TokenResponse]:

    result =await service.login(
        username=form.username, 
        password=form.password.get_secret_value(),

    )

    return success(message="Login successful", data=result)