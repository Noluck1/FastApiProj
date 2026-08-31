from anyio import to_thread
from datetime import datetime, timezone
from app.application.i_unit_of_work import IUnitOfWork
from app.auth.auth_exceptions import UsernameAlreadyExistsError, InvalidCredentialsError, InactiveUserError
from app.auth.i_user_repository import IUserRepository
from app.auth.password import password_hash, hash_password, verify_password, DUMMY_PASSWORD_HASH
from app.auth.token_service import TokenService
from app.shared.dtos.auth_dto import RegisterRequest, UserDto, TokenResponse
from app.auth.i_refresh_token_repository import IRefreshTokenRepository
from app.auth.refresh_token_service import RefreshTokenService




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
    ) -> UserDto:
        async with self._uow:
            existing_user = await self._repository.get_by_username(data.username)

            if existing_user is not None:
                raise UsernameAlreadyExistsError(username=data.username)

            password_hash = await to_thread.run_sync(
                hash_password,
                data.password.get_secret_value(),
            )

            user = await self._repository.add(
                username=data.username,
                password_hash=password_hash,
            )

            await self._uow.commit()

            return user

    async def login(
        self,
        username: str,
        password: str,
    ) -> tuple[TokenResponse, str]:
        async with self._uow:
            user = await self._repository.get_by_username(username)

            stored_hash = (
                user.password_hash
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

            if not user.is_active:
                raise InactiveUserError

            access_token = self._token_service.create_access_token(
                user.id
            )
                
            (
                raw_refresh_token, 
                refresh_token_hash, 
                expires_at,
            ) = self._refresh_token_service.create()

            await self._refresh_repository.add(
                user_id=user.id,
                token_hash=refresh_token_hash,
                expires_at=expires_at,
            )

            await self._uow.commit()
                 
            

            return (
                TokenResponse(access_token=access_token), 
                raw_refresh_token
            )


    async def get_current_user(
        self,
        token: str,
    ) -> UserDto:
        user_id = self._token_service.get_user_id(token)

        async with self._uow:
            user = await self._repository.get_by_id(user_id)

            if user is None:
                raise InvalidCredentialsError

            if not user.is_active:
                raise InactiveUserError
            

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


            if not user.is_active:
                raise InactiveUserError

            new_raw_token, new_token_hash, expires_at = self._refresh_token_service.create()


            await self._refresh_repository.add(
                user_id=user.id,
                token_hash=new_token_hash,
                expires_at=expires_at,
            )

            access_token = self._token_service.create_access_token(user.id)

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