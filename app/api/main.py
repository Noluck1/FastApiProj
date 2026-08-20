from fastapi import FastAPI, Request
from dishka.integrations.fastapi import setup_dishka
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.shared.config.database import create_tables, delete_tables
from app.api.routers.book import router as book_router
from app.application.exceptions import NotFoundError
from app.api.dependency_injection.container import build_container
from collections.abc import AsyncIterator

containter = build_container()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    await app.state.dishka_container.close()
    print("База очищена")


app = FastAPI(lifespan=lifespan)

setup_dishka(
    container=containter,
    app=app,
)

app.include_router(book_router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"Книга '{exc.id}' на найдена."}
    )    