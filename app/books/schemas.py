from pydantic import BaseModel, ConfigDict

class SBookId(BaseModel):
    id: int

class SBooksAdd(BaseModel):
    title: str
    author: str

class SBooks(SBooksAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SBooksUpdate(BaseModel):
    title: str | None
    author: str | None
