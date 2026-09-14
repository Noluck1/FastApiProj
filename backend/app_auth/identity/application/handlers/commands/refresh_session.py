import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from backend.shared.application.port.i_handler import IHandler
from backend.app_auth.identity.api.dto.auth_dto import TokenResponse
from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.app_auth.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_auth.identity.infrastructure.security.token_service import TokenService
from backend.app_auth.identity.infrastructure.security.refresh_token_service import RefreshTokenService
from backend.app_auth.identity.application.exceptions import InvalidCredentialsError
from backend.app_auth.identity.domain.entities.refresh_session import RefreshSession

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class RefreshSessionCommand:
    raw_refresh_token: str


class RefreshSessionHandler(IHandler[RefreshSessionCommand, tuple[TokenResponse, str]]):
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


    async def handle(self, request: RefreshSessionCommand) -> tuple[TokenResponse, str]:
        now = datetime.now(timezone.utc)

        token_hash = self._refresh_token_service.hash(
             request.raw_refresh_token
        )

        async with self._uow:
            stored_token = (
                  await self._refresh_repository.get_by_hash(
                       token_hash
                  )
            )

            if stored_token is None:
                raise InvalidCredentialsError

            revoked = await self._refresh_repository.revoke_active(
                 token_hash=token_hash,
                 revoked_at=now
            )

            if not revoked:
                raise InvalidCredentialsError

            user = await self._repository.get_by_id(
                 stored_token.user_id
            )

            if user is None:
                raise InvalidCredentialsError

            user.ensure_active()
            user_id = user.require_id()

            new_raw_token, new_token_hash, expires_at = self._refresh_token_service.create()

            refresh_session = RefreshSession(
                id=None,
                user_id=user_id,
                token_hash=new_token_hash,
                expires_at=expires_at,
            )

            await self._refresh_repository.add(
                 refresh_session
            )

            access_token = self._token_service.create_access_token(
                user_id,
                roles=frozenset({user.role.value}),
            )

            await self._uow.commit()

            logger.info(
                "Token refreshed successfully: user_id=%s",
                user_id,
            )

            return TokenResponse(access_token=access_token), new_raw_token