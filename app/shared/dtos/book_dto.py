from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class SBookId(BaseModel):
    id: int

class SBooksAdd(BaseModel):
    title: str = Field(
        min_length=5, 
        max_length=100,
    )
    description: str | None = Field(
        default=None, 
        max_length=255,
    )

class SBooks(SBooksAdd):
    id: int 
    model_config = ConfigDict(from_attributes=True)

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

    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)