class UsernameAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class ForbiddenError(Exception):
    pass