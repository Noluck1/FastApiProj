from hmac import compare_digest
from typing import Annotated
import logging

from fastapi import Header, status, HTTPException
from backend.app_auth.identity.config.settings import identity_settings

logger = logging.getLogger(__name__)

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
        logger.warning(
            "Internal service authentication rejected: "
            "reason=missing_token"
            if service_token is None
            else "Internal service authentication rejected: "
                "reason=invalid_token"
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token",
        )