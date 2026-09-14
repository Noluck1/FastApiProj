from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, SecretStr, StringConstraints, model_validator
from backend.app_auth.identity.domain.enums.user_role import UserRole

NamePart = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=50,
    )

    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):
    username: str = Field(
            min_length=5,
            max_length=50,
    )
    
    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

class UserDto(BaseModel):
    id: int
    username: str
    role: UserRole
    is_active: bool

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UpdateFullNameRequest(BaseModel):
    first_name: NamePart | None = None
    last_name: NamePart | None = None
    middle_name: NamePart | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_patch(self) -> "UpdateFullNameRequest":
        fields = self.model_fields_set

        if not fields:
            raise ValueError(
                "At least one full name field must be provided"
            )

        if "first_name" in fields and self.first_name is None:
            raise ValueError(
                "First name cannot be null"
            )
        
        if (
            "last_name" in fields
            and self.last_name is None
        ):
            raise ValueError(
                "Last name cannot be null"
            )

        return self
 