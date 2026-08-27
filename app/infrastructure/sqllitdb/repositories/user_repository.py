from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.enums.user_role import UserRole
from app.auth.i_user_repository import IUserRepository
from app.infrastructure.sqllitdb.models import UserOrm
from app.shared.dtos.auth_dto import UserWithPasswordDto, UserDto



class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(
        self,
        username: str,
     ) -> UserWithPasswordDto | None:
        result = await self._session.execute(select(UserOrm).where(UserOrm.username == username))
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return UserWithPasswordDto.model_validate(user)

    async def get_by_id(
            self,
            user_id: int
    ) -> UserDto | None:
        user = await self._session.get(UserOrm, user_id)

        if user is None:
            return None

        return UserDto.model_validate(user)


    async def add(
            self,
            username: str,
            password_hash: str
    ) -> UserDto:
        user = UserOrm(
            username=username,
            password_hash=password_hash,
            role=UserRole.USER,
            is_active=True,
        )

        self._session.add(user)
        await self._session.flush()

        return UserDto.model_validate(user)