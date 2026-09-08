from fastapi import FastAPI

from app_auth.identity.api.routers.auth import router as auth_router
from app_auth.identity.api.exception_handlers import register_identity_exception_handlers
from app_auth.identity.api.routers.internal_users import router as internal_user_router

def register_identity_api(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(internal_user_router)

    register_identity_exception_handlers(app)
