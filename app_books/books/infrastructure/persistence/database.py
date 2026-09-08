from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app_books.books.config.settings import books_settings


books_engine = create_async_engine(
    books_settings.database_url
)

if books_engine.url.get_backend_name() == "sqlite":
    @event.listens_for(books_engine.sync_engine, "connect")
    def enable_sqlite_foreign_keys(
        dbapi_connection: object,
        _connection_record: object,
    ) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


books_session_factory = async_sessionmaker(
    books_engine,
    expire_on_commit=False,
)