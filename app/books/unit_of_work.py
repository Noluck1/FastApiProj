from app.shared.config.database import new_session
from app.infrastructure.sqllitdb.repositories.book_repository import BookRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = new_session

    async def __aenter__(self):
        self.session = self.session_factory()
        self.books = BookRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()