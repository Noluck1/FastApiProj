from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from backend.app_auth.identity.api.routers.internal_users import router as internal_users_router
from backend.app_auth.identity.application.handlers.queries.get_user_status import GetUserStatusHandler
from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.app_auth.identity.infrastructure.persistence.base import IdentityBase
from backend.app_auth.identity.infrastructure.persistence.repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def identity_session_factory(
    tmp_path: Path,
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database_path = tmp_path / "identity-test.db"

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database_path.as_posix()}"
    )

    async with engine.begin() as connection:
        await connection.run_sync(
            IdentityBase.metadata.create_all
        )

    factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    yield factory

    await engine.dispose()

@pytest_asyncio.fixture
async def identity_client(
    identity_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[httpx.AsyncClient]:
    factory = identity_session_factory

    class TestIdentetyProvider(Provider):
        @provide(scope=Scope.REQUEST)
        async def session(
            self,
        ) -> AsyncIterator[AsyncSession]:
            async with factory() as session:
                yield session

        @provide(scope=Scope.REQUEST)
        def user_repository(
            self,
            session: AsyncSession,
        ) -> IUserRepository:
            return UserRepository(session)

        @provide(scope=Scope.REQUEST)
        def get_user_status_handler(
            self,
            repository: IUserRepository,
        ) -> GetUserStatusHandler:
            return GetUserStatusHandler(repository)

    container = make_async_container(
        TestIdentetyProvider()
    )

    app = FastAPI()

    setup_dishka(
        container=container,
        app=app,
    )

    app.include_router(internal_users_router)

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://identity-test",
    ) as client:
        yield client
    await container.close()
