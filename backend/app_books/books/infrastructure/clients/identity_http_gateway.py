import httpx
import logging
from time import perf_counter
from pydantic import BaseModel, ValidationError

from backend.app_books.books.application.exceptions import IdentityServiceUnvailableError
from backend.app_books.books.application.ports.outbound.i_identity_gateway import IdentityUser, IIdentityGateway

logger = logging.getLogger(__name__)

class IdentityUserResponse(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    is_active: bool
    roles: list[str]

class IdentityHttpGateway(IIdentityGateway):
    def __init__(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        self._client = client

    async def get_user(
        self, 
        user_id: int
    ) -> IdentityUser | None:
        started_at = perf_counter()
        try:
            response = await self._client.get(
                f"/internal/users/{user_id}"
            )

        except httpx.RequestError as error:
            logger.warning(
                "Identity request failed: opperation=get_user "
                "user_id=%s reason=timeout duration_ms=%.2f",
                user_id,
                (perf_counter() - started_at) * 1000,
            )
            raise IdentityServiceUnvailableError from error

        if response.status_code == 404:
            logger.debug(
                "Identity user not found: user_id=%s duration_ms=%.2f",
                user_id,
                (perf_counter() - started_at) * 1000,
            )
            return None

        if response.status_code != 200:
            logger.error(
                "Identity request failed: operation=get_user" 
                "user_id=%s statuse_code=%s duration_ms%.2f",
                user_id,
                response.status_code,
                (perf_counter() - started_at) * 1000,
            )
            raise IdentityServiceUnvailableError

        try:
            data = IdentityUserResponse.model_validate(
                response.json()
            )

        except (ValidationError, ValueError) as error:
            logger.exception(
                "Invalid identity response: operation=get_user "
                "user_id=%s status_code=%s",
                user_id,
                response.status_code,
            )
            raise IdentityServiceUnvailableError from error

        return IdentityUser(
            user_id=data.id,
            username=data.username,
            full_name=data.full_name,
            is_active=data.is_active,
            roles=frozenset(data.roles)
        )
