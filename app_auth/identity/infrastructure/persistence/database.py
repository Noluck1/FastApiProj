from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app_auth.identity.config.settings import identity_settings

identity_engine = create_async_engine(identity_settings.database_url)

if identity_engine.url.get_backend_name() == "sqlite":
    @event.listens_for(identity_engine.sync_engine, "connect")
    def enable_sqlite_foreign_keys(
        dbapi_connection: object,
        _connection_record: object,
    ) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


identity_session_factory = async_sessionmaker(
    identity_engine,
    expire_on_commit=False,
)