from hmac import compare_digest
from typing import Annotated

from fastapi import Header, status, HTTPException
from app_auth.identity.config.settings import identity_settings


async def require_service_token(
    service_token: Annotated[
        str | None,
        Header(alias="X-Service-Token"),
    ] = None,
) -> None:
    expected = (
        identity_settings
        .internal_service_token
        .get_secret_value()
    )

    if (
        service_token is None
        or not compare_digest(service_token, expected)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token",
        )