from pydantic import BaseModel, Field, ConfigDict, SecretStr
from app.shared.enums.user_role import UserRole

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

    model_config = ConfigDict(from_attributes=True)

class UserWithPasswordDto(UserDto):
    password_hash: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'