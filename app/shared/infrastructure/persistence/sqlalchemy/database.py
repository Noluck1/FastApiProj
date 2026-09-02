from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.shared.infrastructure.persistence.sqlalchemy.base import Model
from app.shared.config.settings import settings
from sqlalchemy import event

engine = create_async_engine(settings.database_url)

if engine.url.get_backend_name() == "sqlite":
    @event.listens_for(engine.sync_engine, "connect")
    def enavle_sqlite_foreign_keys(
        dbapi_connection,
        _connection_record,
    ) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

