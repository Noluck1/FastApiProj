import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app_auth.identity.config.settings import identity_settings
from backend.app_auth.identity.domain.enums.user_role import UserRole
from backend.app_auth.identity.infrastructure.persistence.models.user_model import UserOrm


async def create_user(
    factory: async_sessionmaker[AsyncSession],
    *,
    user_id: int,
    is_active: bool = True,
    role: UserRole = UserRole.USER,
    first_name: str | None = None,
    last_name: str | None = None,
    middle_name: str | None = None,
) -> None:
    async with factory() as session:
        session.add(
            UserOrm(
                id=user_id,
                username=f"user-{user_id}",
                password_hash="test-password-hash",
                role=role,
                is_active=is_active,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
            )
        )

        await session.commit()

def service_heders() -> dict[str, str]:
    token = (
        identity_settings
        .internal_service_token
        .get_secret_value()
    )

    return {
        "X-Service-Token": token,
    }

@pytest.mark.asyncio
async def test_returns_existing_user(
    identity_client: httpx.AsyncClient,
    identity_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    await create_user(
        identity_session_factory,
        user_id=42,
        role=UserRole.AUTHOR,
        first_name="Иван",
        last_name="Петров",
        middle_name="Сергеевич",
    )

    response = await identity_client.get(
        "/internal/users/42",
        headers=service_heders(),
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 42,
        "username": "user-42",
        "full_name": "Петров Иван Сергеевич",
        "is_active": True,
        "roles": ["author"],
    }

@pytest.mark.asyncio
async def test_returns_inactive_user_status(
    identity_client: httpx.AsyncClient,
    identity_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    await create_user(
        identity_session_factory,
        user_id=42,
        is_active=False,
    )

    response = await identity_client.get(
        "/internal/users/42",
        headers=service_heders(),
    )

    assert response.status_code == 200
    assert response.json()["id"] == 42
    assert response.json()["is_active"] is False

@pytest.mark.asyncio
async def test_returns_404_for_unknown_user(
    identity_client: httpx.AsyncClient,
) -> None:
    response = await identity_client.get(
        "/internal/users/999",
        headers=service_heders(),
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found",
    }

@pytest.mark.asyncio
async def test_rejects_invalid_service_token(
    identity_client: httpx.AsyncClient,
) -> None:
    response = await identity_client.get(
        "/internal/users/42",
        headers={
            "X-Service-Token": "wrong-token",
        },
    )

    assert response.status_code == 401
