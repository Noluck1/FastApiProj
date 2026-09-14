from dishka import FromDishka
from typing import Annotated
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app_auth.identity.api.dto.internal_user_dto import InternalUserStatusResponse
from backend.app_auth.identity.application.handlers.queries.get_user_status import GetUserStatusQuery, GetUserStatusHandler
from backend.app_auth.identity.infrastructure.security.require_service_token import require_service_token

router = APIRouter(
    prefix="/internal/users",
    tags=["Internal"],
    route_class=DishkaRoute
)


@router.get("/{user_id}", response_model=InternalUserStatusResponse, include_in_schema=False)
async def get_user_status(
    user_id: int,
    handler: FromDishka[GetUserStatusHandler],
    _authorized: Annotated[
        None,
        Depends(require_service_token),
    ],
) -> InternalUserStatusResponse:
    result = await handler.handle(
        GetUserStatusQuery(user_id=user_id)
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return InternalUserStatusResponse(
        id=result.user_id,
        username=result.username,
        full_name=result.full_name,
        is_active=result.is_active,
        roles=sorted(result.roles)
    )
