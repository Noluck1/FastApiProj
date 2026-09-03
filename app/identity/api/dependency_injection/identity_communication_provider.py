from dishka import Provider, Scope, provide
from app.communication.identity.i_identity_communication import IIdentityCommunication
from app.identity.application.ports.i_user_repository import IUserRepository
from app.identity.application.services.identity_communication import IdentityCommunication


class IdentityCommunicationProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def identity_communication(
        self,
        repository: IUserRepository,
    ) -> IIdentityCommunication:
        return IdentityCommunication(repository)