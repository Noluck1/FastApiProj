import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app_auth.identity.api.dependency_injection.container import build_identity_container
from backend.app_auth.identity.api.setup import register_identity_api
from backend.app_auth.identity.config.settings import identity_settings
from backend.app_auth.identity.infrastructure.persistence.database import identity_engine

from backend.shared.api.exception_handler import register_common_exception_handlers
from backend.shared.config.logging_config import configure_logging

configure_logging(identity_settings.log_level)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    container = build_identity_container()

    @asynccontextmanager
    async def lifespan(
        _app: FastAPI,
    ) -> AsyncIterator[None]:
        logger.info("Identity service started")

        try:
            yield
        finally:
            await container.close()
            await identity_engine.dispose()

            logger.info("Identity service stopped")

    application = FastAPI(
        title="Identity service",
        lifespan=lifespan
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8002",
            "http://127.0.0.1:8002",

            "http://localhost:8010",
            "http://127.0.0.1:8010",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_dishka(
        container=container,
        app=application,
    )

    register_common_exception_handlers(application)
    register_identity_api(application)

    return application

app = create_app()