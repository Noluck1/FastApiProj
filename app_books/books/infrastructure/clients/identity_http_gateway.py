import httpx
from pydantic import BaseModel, ValidationError

from app_books.books.application.exceptions import IdentityServiceUnvailableError
from app_books.books.application.ports.outbound.i_identity_gateway import IdentityUser, IIdentityGateway

class IdentityUserResponse(BaseModel):
    id: int
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
        try:
            response = await self._client.get(
                f"/internal/users/{user_id}"
            )

        except httpx.RequestError as error:
            raise IdentityServiceUnvailableError from error

        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise IdentityServiceUnvailableError

        try:
            data = IdentityUserResponse.model_validate(
                response.json()
            )

        except (ValidationError, ValueError) as error:
            raise IdentityServiceUnvailableError from error

        return IdentityUser(
            user_id=data.id,
            is_active=data.is_active,
            roles=frozenset(data.roles)
        )