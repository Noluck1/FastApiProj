class FavoriteNotFoundError(Exception):
    def __init__(self, user_id: int, book_id: int) -> None:
        self.user_id = user_id
        self.book_id = book_id