import logging
from anyio import to_thread
from dataclasses import dataclass 
from backend.shared.application.port.i_handler import IHandler
from backend.app_auth.identity.domain.entities.user import User
from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_auth.identity.domain.value_objects.username import Username
from backend.app_auth.identity.application.exceptions import UsernameAlreadyExistsError
from backend.app_auth.identity.infrastructure.security.password import hash_password
from backend.app_auth.identity.domain.value_objects.password_hash import PasswordHash
from backend.app_auth.identity.domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    password: str


class RegisterUserHandler(IHandler[RegisterUserCommand, User]):
    def __init__(self, repository: IUserRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: RegisterUserCommand) -> User:
        async with self._uow:
            username = Username(request.username)

            existing_user = await self._repository.get_by_username(username)

            if existing_user is not None:
                raise UsernameAlreadyExistsError(username=username.value)

            hashed_password = await to_thread.run_sync(
                hash_password,
                request.password,
            )
        
            user = User(
                id=None,
                username=username,
                password_hash=PasswordHash(hashed_password),
                role=UserRole.USER,
                is_active=True
            )

            saved_user = await self._repository.add(user)

            await self._uow.commit()

            logger.info(
                "User register: user_id=%s",
                saved_user.require_id(),
            )
            
            return saved_user