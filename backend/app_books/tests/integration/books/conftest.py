from collections.abc import AsyncIterator
from pathlib import Path
from unittest.mock import MagicMock
import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


from backend.app_books.books.infrastructure.persistence.models.book.book_model import (
    BooksOrm,
)
from backend.app_books.books.infrastructure.persistence.models.favorite.favorite_books_model import (
    FavoriteBookOrm,
)

from backend.app_books.books.infrastructure.persistence.base import BooksBase



@pytest_asyncio.fixture
async def session_factory(
    tmp_path: Path,
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database_path = tmp_path / "test.db"

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database_path.as_posix()}"
    )

    @event.listens_for(engine.sync_engine, "connect")
    def enable_foreign_keys(
        dbapi_connection: object,
        connection_record: object,
    ) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as connection:
        await connection.run_sync(
            BooksBase.metadata.create_all
        )

    factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    yield factory

    await engine.dispose()