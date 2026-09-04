from fastapi import FastAPI

from app.identity.api.routers.auth import router as auth_router
from app.identity.api.exception_handlers import register_identity_exception_handlers


def register_identity_api(app: FastAPI) -> None:
    app.include_router(auth_router)
    register_identity_exception_handlers(app)