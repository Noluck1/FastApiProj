from datetime import datetime, timezone
from dataclasses import dataclass
from app.identity.application.handlers.i_handler import IHandler
from app.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from app.identity.infrastructure.security.refresh_token_service import RefreshTokenService
from app.shared.application.port.i_unit_of_work import IUnitOfWork



@dataclass(frozen=True)
class LogoutUserCommand:
    raw_refresh_token: str


class LogoutUserHandler(IHandler[LogoutUserCommand, None]):
    def __init__(
        self, 
        refresh_repository: IRefreshTokenRepository, 
        refresh_token_service: RefreshTokenService,
        uow: IUnitOfWork,
    ):
        self._refresh_token_service = refresh_token_service
        self._refresh_repository = refresh_repository
        self._uow = uow


    async def handle(self, request: LogoutUserCommand) -> None:
        token_hash = self._refresh_token_service.hash(
            request.raw_refresh_token
        )

        async with self._uow:
            await self._refresh_repository.revoke_active(
                token_hash=token_hash,
                revoked_at=datetime.now(timezone.utc)
            )

            await self._uow.commit()

        
        


