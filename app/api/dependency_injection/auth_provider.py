from dishka import Provider, Scope, provide

from app.application.i_unit_of_work import IUnitOfWork
from app.auth.auth_service import AuthService
from app.auth.i_user_repository import IUserRepository
from app.auth.token_service import TokenService
from app.shared.config.settings import settings
from app.auth.i_refresh_token_repository import IRefreshTokenRepository
from app.auth.refresh_token_service import RefreshTokenService


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
        refresh_repository: IRefreshTokenRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
        refresh_token_service: RefreshTokenService,
    ) -> AuthService:
        return AuthService(
            repository=repository,
            refresh_repository=refresh_repository,
            uow=uow,
            token_service=token_service,
            refresh_token_service=refresh_token_service,
        )

    @provide(scope=Scope.APP)
    def refresh_token_service(self) -> RefreshTokenService:
        return RefreshTokenService(
            expire_days=settings.refresh_token_expire_days,
        )