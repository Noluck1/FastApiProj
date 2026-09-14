from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class SBooksAdd(BaseModel):
    title: str = Field(
        min_length=5, 
        max_length=100,
    )
    description: str | None = Field(
        default=None, 
        max_length=255,
    )

class SBooksUpdate(BaseModel):
    title: str | None = Field(
        default=None, 
        min_length=5,
    )
    description: str | None = Field(
        default=None, 
        max_length=255,
    )

class SPutBookUpdate(BaseModel):
    title: str
    description: str

class BooksDto(BaseModel):
    id: int
    title: str
    description: str | None
    author_id: int
    author_username: str | None = None
    author_full_name: str | None = None

    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

