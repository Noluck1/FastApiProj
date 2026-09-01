from anyio import to_thread
from datetime import datetime, timezone
from app.application.i_unit_of_work import IUnitOfWork
from app.auth.auth_exceptions import UsernameAlreadyExistsError, InvalidCredentialsError
from app.auth.i_user_repository import IUserRepository
from app.auth.password import hash_password, verify_password, DUMMY_PASSWORD_HASH
from app.auth.token_service import TokenService
from app.shared.dtos.auth_dto import RegisterRequest, TokenResponse
from app.auth.i_refresh_token_repository import IRefreshTokenRepository
from app.auth.refresh_token_service import RefreshTokenService
from app.domain.auth.entities.user import User
from app.domain.auth.value_objects.username import Username
from app.domain.auth.value_objects.password_hash import PasswordHash
from app.domain.auth.enums.user_role import UserRole
from app.domain.auth.entities.refresh_session import RefreshSession


class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        refresh_repository: IRefreshTokenRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self._repository = repository
        self._refresh_repository = refresh_repository
        self._uow = uow
        self._token_service = token_service
        self._refresh_token_service = refresh_token_service


    async def register(
        self,
        data: RegisterRequest,
    ) -> User:
        async with self._uow:
            username = Username(data.username)

            existing_user = await self._repository.get_by_username(username)

            if existing_user is not None:
                raise UsernameAlreadyExistsError(username=username.value)

            hashed_password = await to_thread.run_sync(
                hash_password,
                data.password.get_secret_value(),
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

            return saved_user

    async def login(
        self,
        username: str,
        password: str,
    ) -> tuple[TokenResponse, str]:
        async with self._uow:

            username_value = Username(username)

            user = await self._repository.get_by_username(username_value)

            stored_hash = (
                user.password_hash.value
                if user is not None
                else DUMMY_PASSWORD_HASH
            )

            password_is_valid = await to_thread.run_sync(
                verify_password,
                password,
                stored_hash,
            )

            if user is None or not password_is_valid:
                raise InvalidCredentialsError

            user.ensure_active()
            user_id = user.require_id()

            access_token = self._token_service.create_access_token(
                user_id
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
                expires_at=expires_at
            )

            await self._refresh_repository.add(
                refresh_session
            )

            await self._uow.commit()
                 
            

            return (
                TokenResponse(access_token=access_token), 
                raw_refresh_token
            )


    async def get_current_user(
        self,
        token: str,
    ) -> User:
        user_id = self._token_service.get_user_id(token)

        async with self._uow:
            user = await self._repository.get_by_id(user_id)

            if user is None:
                raise InvalidCredentialsError

            user.ensure_active()
            
            return user

    async def refresh(
            self,
            raw_refresh_token: str,
    ) -> tuple[TokenResponse, str]:
        now = datetime.now(timezone.utc)

        token_hash = self._refresh_token_service.hash(
                raw_refresh_token
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
                revoked_at=now,
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

            access_token = self._token_service.create_access_token(user_id)

            await self._uow.commit()

            return TokenResponse(access_token=access_token), new_raw_token

    async def logout(
            self,
            raw_refresh_token: str,
    ) -> None:
        token_hash = self._refresh_token_service.hash(
                raw_refresh_token
            )
        

        async with self._uow:
            await self._refresh_repository.revoke_active(
                token_hash=token_hash,
                revoked_at=datetime.now(timezone.utc),
            )

            await self._uow.commit()