from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Self

class SBookId(BaseModel):
    id: int

class SBooksAdd(BaseModel):
    title: str = Field(min_length=5)
    author: str = Field(min_length=5)

class SBooks(SBooksAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SBooksUpdate(BaseModel):
    title: str | None
    author: str | None 
