from dataclasses import dataclass
import jwt
from jwt.exceptions import InvalidTokenError

class InvalidAccessTokenError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class AccessTokenClaims:
    subject_id: int
    roles: frozenset[str]

class AccessTokenVerifier:
    def __init__(
        self,
        public_key: str,
        algorithm: str,
        issuer: str,
        audience: str,
    ) ->None:
        self._public_key = public_key
        self._algorithm = algorithm
        self._issuer = issuer
        self._audience = audience

    def verify(self, token: str) -> AccessTokenClaims:
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
                        "roles",
                        "type",
                        "iat",
                        "exp",
                        "iss",
                        "aud",
                    ],
                },
            )

            if payload["type"] != "access":
                raise InvalidAccessTokenError

            roles = payload["roles"]

            if not isinstance(roles, list):
                raise InvalidAccessTokenError

            return AccessTokenClaims(
                subject_id=int(payload["sub"]),
                roles=frozenset(str(role) for role in roles),
            )
        except (
            InvalidTokenError,
            KeyError,
            TypeError,
            ValueError
        ) as error:
            raise InvalidAccessTokenError from error