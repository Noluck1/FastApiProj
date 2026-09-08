from dataclasses import dataclass
from app_auth.identity.domain.entities.user import User
from shared.application.port.i_handler import IHandler
from app_auth.identity.infrastructure.security.token_service import TokenService
from app_auth.identity.application.ports.i_user_repository import IUserRepository
from app_auth.identity.application.exceptions import InvalidCredentialsError

@dataclass(frozen=True)
class GetCurrentUserCommand:
    token: str


class GetCurrentUserHandler(IHandler[GetCurrentUserCommand, User]):
    def __init__(
        self, 
        token_service: TokenService, 
        repository: IUserRepository, 
    ):
        self._repository = repository
        self._token_service = token_service


    async def handle(self, request: GetCurrentUserCommand) -> User:
        user_id = self._token_service.get_user_id(request.token)
        
        user = await self._repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError

        user.ensure_active()

        return user
        
