from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest
from backend.app_books.books.application.handlers.books.command.cleanup import BookCleanupCommand, BookCleanupHandler


@pytest.mark.asyncio
async def test_cleanup_deletes_books_before_cutoff(
    repository: MagicMock,
    uow: MagicMock,
) -> None:
    fixed_now = datetime(
        2026,
        9,
        4,
        12,
        0,
        tzinfo=timezone.utc,
    )

    repository.purge_deleted_before.return_value = 3

    handler = BookCleanupHandler(
        repository=repository,
        uow=uow,
    )

    with patch(
        "app_books.books.application.handlers.books.command.cleanup.datetime"
    ) as datetime_mock:
        datetime_mock.now.return_value = fixed_now

        result = await handler.handle(
            BookCleanupCommand(retention_days=30)
        )

    expected_cutoff = fixed_now - timedelta(days=30)

    assert result == 3

    repository.purge_deleted_before.assert_awaited_once_with(
        expected_cutoff
    )

    uow.commit.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_cleanup_does_not_commit_when_repository_fails(
    repository: MagicMock,
    uow: MagicMock,
) -> None:
    repository.purge_deleted_before.side_effect = RuntimeError(
        "Database error"
    )

    handler = BookCleanupHandler(
        repository=repository,
        uow=uow,
    )

    with pytest.raises(RuntimeError, match="Database error"):
        await handler.handle(
            BookCleanupCommand(retention_days=30)
        )

    uow.commit.assert_not_awaited()