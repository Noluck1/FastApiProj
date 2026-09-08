from pydantic import BaseModel

class InternalUserStatusResponse(BaseModel):
    id: int
    is_active: bool
    roles: list[str]
