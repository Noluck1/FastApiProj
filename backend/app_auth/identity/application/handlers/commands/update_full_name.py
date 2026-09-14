from dataclasses import dataclass
from backend.app_auth.identity.domain.entities.user import User
from backend.shared.application.port.i_handler import IHandler
from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.shared.application.port.i_unit_of_work import IUnitOfWork
from backend.app_auth.identity.application.exceptions import InvalidCredentialsError

@dataclass(frozen=True, slots=True)
class UpdateFullNameCommand:
    user: User
    fields: frozenset[str]

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


class UpdateFullNameHandler(IHandler[UpdateFullNameCommand, User]):
    def __init__(
        self, 
        repository: IUserRepository, 
        uow: IUnitOfWork
    ):
        self._repository = repository
        self._uow = uow

    async def handle(self, request: UpdateFullNameCommand) -> User:
        async with self._uow:
            user = request.user
            user.ensure_active()

            if "first_name" in request.fields:
                if request.first_name is None:
                    raise ValueError(
                        "First name cannot be null"
                    )
                user.change_first_name(
                    request.first_name
                )

            if "last_name" in request.fields:
                if request.last_name is None:
                    raise ValueError(
                        "Last name cannot be null"
                    )

                user.change_last_name(
                    request.last_name
                )

            if "middle_name" in request.fields:
                if request.middle_name is None:
                    raise ValueError(
                        "Middle name cannot be null"
                    )

                user.change_middle_name(
                    request.middle_name
                )

            saved_user = await self._repository.save(user)

            if saved_user is None:
                raise InvalidCredentialsError

            await self._uow.commit()

            return saved_user