from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infrastructure.sqllitdb.base import Model
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  database_url: str

  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

engine = create_async_engine(settings.database_url)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

