class ForbiddenError(Exception):
    def __init__(self, role: str):
        self.role = role


class UnAuthorizedError(Exception):
    pass