from fastapi import Response
from app.shared.config.settings import settings



def set_refresh_cookie(
    response: Response,
    refresh_token: str,
) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite="lax",
        path="/auth",
        max_age=(
            settings.refresh_token_expire_days
            *24
            *60
            *60
        ),
    )