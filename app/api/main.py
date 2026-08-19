from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.shared.config.database import create_tables, delete_tables
from app.api.routers.book import router as book_router
from app.books.exceptions import NotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")
app = FastAPI(lifespan=lifespan)
app.include_router(book_router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Книга '{exc.id}' на найдена."}
    )    