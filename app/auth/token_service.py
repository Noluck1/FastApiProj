from datetime import datetime, timezone, timedelta
from importlib.metadata import requires
from uuid import uuid4

import jwt
from jwt import InvalidTokenError

from app.auth.auth_exceptions import InvalidCredentialsError


class TokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
        issuer: str,
        audience: str
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes
        self._issuer = issuer
        self._audience = audience

    def create_access_token(self, user_id: int) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
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
            self._secret_key,
            algorithm=self._algorithm,
        )

    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                issuer=self._issuer,
                audience=self._audience,
                options={
                    "requires": [
                        "sub",
                        "type",
                        "iat",
                        "exp",
                        "iss",
                        "aud",
                    ]
                },
            )

            if payload["type"] == "access":
                raise InvalidCredentialsError

            return int(payload["sub"])

        except (
            InvalidTokenError,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            raise InvalidCredentialsError from error