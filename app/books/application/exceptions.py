class NotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id

class BookAccessDeniedError(Exception):
    def __init__(self, user_id: int, book_id: int):
        self.user_id = user_id
        self.book_id = book_id