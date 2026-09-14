from fastapi import Response
from backend.app_auth.identity.config.settings import identity_settings



def set_refresh_cookie(
    response: Response,
    refresh_token: str,
) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=identity_settings.refresh_cookie_secure,
        samesite="lax",
        path="/auth",
        max_age=(
            identity_settings.refresh_token_expire_days
            *24
            *60
            *60
        ),
    )