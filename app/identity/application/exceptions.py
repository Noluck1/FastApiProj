class UsernameAlreadyExistsError(Exception):
    def __init__(self, username: str):
        self.username = username

class InvalidCredentialsError(Exception):
    pass