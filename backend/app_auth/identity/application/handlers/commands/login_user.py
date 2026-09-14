import logging
from anyio import to_thread
from dataclasses import dataclass
from backend.shared.application.port.i_handler import IHandler
from backend.app_auth.identity.api.dto.auth_dto import TokenResponse
from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_auth.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from backend.app_auth.identity.infrastructure.security.refresh_token_service import RefreshTokenService
from backend.app_auth.identity.infrastructure.security.token_service import TokenService
from backend.app_auth.identity.domain.value_objects.username import Username
from backend.app_auth.identity.infrastructure.security.password import DUMMY_PASSWORD_HASH, verify_password
from backend.app_auth.identity.application.exceptions import InvalidCredentialsError
from backend.app_auth.identity.domain.entities.refresh_session import RefreshSession

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LoginUserCommand:
    username: str
    password: str


class LoginUserHandler(IHandler[LoginUserCommand, tuple[TokenResponse, str]]):
    def __init__(
            self, 
            repository: IUserRepository, 
            refresh_repository: IRefreshTokenRepository, 
            uow: IUnitOfWork, 
            token_service: TokenService, 
            refresh_token_service: RefreshTokenService,
    ):
        self._repository = repository
        self._refresh_repository = refresh_repository
        self._uow = uow
        self._token_service = token_service
        self._refresh_token_service = refresh_token_service


    async def handle(self, request: LoginUserCommand) -> tuple[TokenResponse, str]:
        async with self._uow:

            username_value = Username(request.username)

            user = await self._repository.get_by_username(username_value)

            stored_hash = (
                user.password_hash.value
                if user is not None
                else DUMMY_PASSWORD_HASH
            )

            password_is_valid = await to_thread.run_sync(
                verify_password,
                request.password,
                stored_hash,
            )

            if user is None or not password_is_valid:
                raise InvalidCredentialsError

            user.ensure_active()
            user_id = user.require_id()

            access_token = self._token_service.create_access_token(
                user_id,
                roles=frozenset({user.role.value}),
            )

            (
                raw_refresh_token,
                refresh_token_hash,
                expires_at,
            ) = self._refresh_token_service.create()

            refresh_session = RefreshSession(
                id=None,
                user_id=user_id,
                token_hash=refresh_token_hash,
                expires_at=expires_at,
            )

            await self._refresh_repository.add(
                refresh_session
            )

            await self._uow.commit()

            logger.info(
                "User login successfully: user_id=%s",
                user_id,
            )

            return (
                TokenResponse(access_token=access_token),
                raw_refresh_token
            )