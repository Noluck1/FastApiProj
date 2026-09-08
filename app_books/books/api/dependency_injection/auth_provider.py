from dishka import Provider, Scope, provide

from app_books.books.config.settings import books_settings
from app_books.books.infrastructure.security.access_token_verifier import AccessTokenVerifier


class BooksAuthProvider(Provider):
    @provide(scope=Scope.APP)
    def access_token_verifier(self) -> AccessTokenVerifier:
        public_key = (
            books_settings.jwt_public_key_path
            .read_text(encoding="utf-8")
        )
        return AccessTokenVerifier(
            public_key=public_key,
            algorithm=books_settings.jwt_algorithm,
            issuer=books_settings.jwt_issuer,
            audience=books_settings.jwt_audience,
        )