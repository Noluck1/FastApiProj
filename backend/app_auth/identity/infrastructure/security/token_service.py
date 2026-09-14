from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError

from backend.app_auth.identity.application.exceptions import InvalidCredentialsError


class TokenService:
    def __init__(
        self,
        private_key: str,
        public_key: str,
        algorithm: str,
        expire_minutes: int,
        issuer: str,
        audience: str
    ) -> None:
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes
        self._issuer = issuer
        self._audience = audience

    def create_access_token(self, user_id: int, roles: frozenset[str]) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "roles": list(roles),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(
                minutes=self._expire_minutes
            ),
            "iss": self._issuer,
            "aud": self._audience,
            "jti": str(uuid4())
        }

        return jwt.encode(
            payload,
            self._private_key,
            algorithm=self._algorithm,
        )

    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self._public_key,
                algorithms=[self._algorithm],
                issuer=self._issuer,
                audience=self._audience,
                options={
                    "require": [
                        "sub",
                        "type",
                        "iat",
                        "exp",
                        "iss",
                        "aud",
                    ]
                },
            )

            if payload["type"] != "access":
                raise InvalidCredentialsError

            return int(payload["sub"])

        except (
            InvalidTokenError,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            raise InvalidCredentialsError from error