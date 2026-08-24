from anyio import to_thread

from app.application.i_unit_of_work import IUnitOfWork
from app.auth.auth_exceptions import UsernameAlreadyExistsError, InvalidCredentialsError, InactiveUserError
from app.auth.i_user_repository import IUserRepository
from app.auth.password import password_hash, hash_password, verify_password, DUMMY_PASSWORD_HASH
from app.auth.token_service import TokenService
from app.shared.dtos.auth_dto import RegisterRequest, UserDto, TokenResponse


class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
    ) -> None:

        self._repository = repository
        self._uow = uow
        self._token_service = token_service


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
    ) -> TokenResponse:
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

            access_token = (
                self._token_service.create_access_token(
                    user.id
                )
            )

            return TokenResponse(access_token=access_token)


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
