class UsernameAlreadyExistsError(Exception):
    def __init__(self, username: str):
        self.username = username

class InvalidCredentialsError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class ForbiddenError(Exception):
    def __init__(self, role: str):
        self.role = role


class UnAuthorizedError(Exception):
    pass


class BookAccessDeniedError(Exception):
    def __init__(self, user_id: int, book_id: int):
        self.user_id = user_id
        self.book_id = book_id
        