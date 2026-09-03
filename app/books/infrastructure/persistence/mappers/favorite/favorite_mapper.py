from app.books.infrastructure.persistence.models.favorite.favorite_books_model import FavoriteBookOrm
from app.books.domain.entities.favorite_entity.favorite_book import FavoriteBook
from app.shared.dtos.favorite_dto import FavoriteDto

def favorite_to_domain(model: FavoriteBookOrm) -> FavoriteBook:
    return FavoriteBook(
        user_id=model.user_id,
        book_id=model.book_id,
    )

def favorite_to_orm(favorite: FavoriteBook) -> FavoriteBookOrm:
    return FavoriteBookOrm(
        user_id=favorite.user_id,
        book_id=favorite.book_id,
    )

def favorite_to_dto(favorite: FavoriteBook) -> FavoriteDto:
    return FavoriteDto(
        user_id=favorite.user_id,
        book_id=favorite.book_id,
    )