from pydantic import BaseModel, ConfigDict

class FavoriteDto(BaseModel):
    user_id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)