from pydantic import BaseModel

class InternalUserStatusResponse(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    is_active: bool
    roles: list[str]
