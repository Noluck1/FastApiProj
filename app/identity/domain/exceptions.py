class InvalidUsernameError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class RefreshSessionExpiredError(Exception):
    pass

class RefreshSessionRevokedError(Exception):
    pass