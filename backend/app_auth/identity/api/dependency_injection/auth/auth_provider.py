from dishka import Provider, Scope, provide

from backend.app_auth.identity.infrastructure.security.token_service import TokenService
from backend.app_auth.identity.config.settings import identity_settings
from backend.app_auth.identity.infrastructure.security.refresh_token_service import RefreshTokenService


class AuthProvider(Provider):
    @provide(scope=Scope.APP)
    def token_service(self) -> TokenService:
        private_key = (
            identity_settings.jwt_private_key_path
            .read_text(encoding="utf-8")
        )
        public_key=(
            identity_settings.jwt_public_key_path
            .read_text(encoding="utf-8")
        )
        return TokenService(
            private_key=private_key,
            public_key=public_key,
            algorithm=identity_settings.jwt_algorithm,
            expire_minutes=(
                identity_settings.access_token_expire_minutes
            ),
            issuer=identity_settings.jwt_issuer,
            audience=identity_settings.jwt_audience,
        )

    @provide(scope=Scope.APP)
    def refresh_token_service(self) -> RefreshTokenService:
        return RefreshTokenService(
            expire_days=identity_settings.refresh_token_expire_days,
        )