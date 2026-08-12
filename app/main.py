from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_tables, delete_tables
from app.books.router import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")
app = FastAPI(lifespan=lifespan)
app.include_router(book_router)