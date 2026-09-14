from fastapi import FastAPI

from backend.app_auth.identity.api.routers.auth import router as auth_router
from backend.app_auth.identity.api.exception_handlers import register_identity_exception_handlers
from backend.app_auth.identity.api.routers.internal_users import router as internal_user_router

def register_identity_api(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(internal_user_router)

    register_identity_exception_handlers(app)
