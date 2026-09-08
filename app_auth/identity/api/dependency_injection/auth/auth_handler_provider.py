from dishka import Provider, Scope, provide
from app_auth.identity.application.ports.i_user_repository import IUserRepository
from app_auth.identity.application.handlers.commands.register_user import RegisterUserHandler
from app_auth.identity.application.ports.i_refresh_token_repository import IRefreshTokenRepository
from app_auth.identity.infrastructure.security.token_service import TokenService
from app_auth.identity.infrastructure.security.refresh_token_service import RefreshTokenService
from app_auth.identity.application.handlers.commands.login_user import LoginUserHandler
from app_auth.identity.application.handlers.commands.refresh_session import RefreshSessionHandler
from app_auth.identity.application.handlers.commands.logout_user import LogoutUserHandler
from app_auth.identity.application.handlers.queries.get_me import GetCurrentUserHandler
from shared.application.port.i_unit_of_work import IUnitOfWork
from app_auth.identity.application.handlers.queries.get_user_status import GetUserStatusHandler


class AuthHandlerProvider(Provider):
    scope = Scope.REQUEST


    @provide
    def register_user_handler(
        self,
        repository: IUserRepository,
        uow: IUnitOfWork,
    ) -> RegisterUserHandler:
        return RegisterUserHandler(repository=repository, uow=uow)

    @provide
    def login_user_handler(
        self,
        repository: IUserRepository,
        refresh_repository: IRefreshTokenRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
        refresh_token_service: RefreshTokenService,
    ) -> LoginUserHandler:
        return LoginUserHandler(
            repository=repository,
            refresh_repository=refresh_repository,
            uow=uow,
            token_service=token_service,
            refresh_token_service=refresh_token_service,
        )

    @provide
    def refresh_session_handler(
        self,
        repository: IUserRepository,
        refresh_repository: IRefreshTokenRepository,
        uow: IUnitOfWork,
        token_service: TokenService,
        refresh_token_service: RefreshTokenService,
    ) -> RefreshSessionHandler:
        return RefreshSessionHandler(
            repository=repository,
            refresh_repository=refresh_repository,
            uow=uow,
            token_service=token_service,
            refresh_token_service=refresh_token_service,
        )


    @provide
    def logout_user_handler(
        self,
        refresh_repository: IRefreshTokenRepository, 
        refresh_token_service: RefreshTokenService,
        uow: IUnitOfWork,
    ) -> LogoutUserHandler:
        return LogoutUserHandler(
            refresh_repository=refresh_repository,
            refresh_token_service=refresh_token_service,
            uow=uow,
        )

    @provide
    def get_current_user_handler(
        self,
        token_service: TokenService, 
        repository: IUserRepository, 
    ) -> GetCurrentUserHandler:
        return GetCurrentUserHandler(
            token_service=token_service,
            repository=repository
        )

    @provide
    def get_user_status_handler(
        self,
        repository: IUserRepository,
    ) -> GetUserStatusHandler:
        return GetUserStatusHandler(
            repository=repository
        )