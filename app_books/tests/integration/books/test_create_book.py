import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from unittest.mock import MagicMock
from app_books.books.application.handlers.books.command.create_book import (
    CreateBookCommand,
    CreateBookHandler,
)
from app_books.books.infrastructure.persistence.models.book.book_model import (
    BooksOrm,
)
from app_books.books.infrastructure.persistence.repositories.book.book_repository import (
    BookRepository,
)
from shared.infrastructure.persistence.sqlalchemy.unit_of_work import (
    UnitOfWork,
)


@pytest.mark.asyncio
async def test_create_book_saves_book_in_database(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        repository = BookRepository(session)
        uow = UnitOfWork(session)

        handler = CreateBookHandler(
            repository=repository,
            uow=uow,
        )

        result = await handler.handle(
            CreateBookCommand(
                title="Clean Code",
                description="A programming book",
                author_id=7,
            )
        )

        book_id = result.require_id()

        assert result.title.value == "Clean Code"
        assert result.description is not None
        assert result.description.value == "A programming book"
        assert result.author_id == 7

    async with session_factory() as verification_session:
        model = await verification_session.get(
            BooksOrm,
            book_id,
        )

        assert model is not None
        assert model.id == book_id
        assert model.title == "Clean Code"
        assert model.description == "A programming book"
        assert model.author_id == 7
        assert model.is_deleted is False