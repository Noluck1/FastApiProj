from dishka import Provider, Scope, provide

from app.identity.infrastructure.security.token_service import TokenService
from app.shared.config.settings import settings
from app.identity.infrastructure.security.refresh_token_service import RefreshTokenService


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

    @provide(scope=Scope.APP)
    def refresh_token_service(self) -> RefreshTokenService:
        return RefreshTokenService(
            expire_days=settings.refresh_token_expire_days,
        )