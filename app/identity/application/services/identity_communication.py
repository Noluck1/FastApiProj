from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.identity.application.ports.i_user_repository import IUserRepository
from app.communication.identity.i_identity_communication import UserReference


class IdentityCommunication(IIdentityCommunication):
    def __init__(
        self,
        repository: IUserRepository,
    ) -> None:
        self._repository = repository

    async def get_active_user(self, user_id: int) -> UserReference | None:
        user = await self._repository.get_by_id(user_id)

        if user is None or not user.is_active:
            return None

        return UserReference(user_id=user.require_id())