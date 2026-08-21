from dishka import Provider, Scope, provide

from app.application.i_unit_of_work import IUnitOfWork
from app.auth.auth_service import AuthService
from app.auth.i_user_repository import IUserRepository
from app.auth.token_service import TokenService
from app.shared.config.settings import settings


class AuthProvider(Provider):
    @provide(scope=Scope.APP)
    def token_service(self) -> TokenService:
        return TokenService(
           secret_key=(
               settings.jwt_secret_key.get_secret_value()
           ),
            algorithm=settings.jwt_algorithm,
            expire_minutes=(
                settings.access_token_expire_minutes
            ),
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        repository: IUserRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
    ) -> AuthService:
        return AuthService(
            repository=repository,
            uow=uow,
            token_service=token_service,
        )
