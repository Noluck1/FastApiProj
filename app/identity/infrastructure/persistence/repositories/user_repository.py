from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.identity.application.ports.i_user_repository import IUserRepository
from app.identity.infrastructure.persistence.models.user_model import UserOrm
from app.identity.domain.entities.user import User
from app.identity.infrastructure.persistence.mappers.user_mapper import user_to_domain, user_to_orm
from app.identity.domain.value_objects.username import Username



class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(
        self,
        username: Username,
     ) -> User | None:
        result = await self._session.execute(select(UserOrm).where(UserOrm.username == username.value))
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return user_to_domain(model)

    async def get_by_id(
            self,
            user_id: int
    ) -> User | None:
        model = await self._session.get(UserOrm, user_id)

        if model is None:
            return None

        return user_to_domain(model)


    async def add(
            self,
            user: User,
    ) -> User:
        model = user_to_orm(user)

        self._session.add(model)
        await self._session.flush()

        return user_to_domain(model)