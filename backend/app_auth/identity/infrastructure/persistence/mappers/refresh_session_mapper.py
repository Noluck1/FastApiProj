from backend.app_auth.identity.domain.entities.refresh_session import RefreshSession
from backend.app_auth.identity.domain.value_objects.refresh_token_hash import RefreshTokenHash
from backend.app_auth.identity.infrastructure.persistence.models.refresh_token_model import RefreshTokenOrm


def refresh_session_to_domain(
    model: RefreshTokenOrm,
) -> RefreshSession:
    return RefreshSession(
        id=model.id,
        user_id=model.user_id,
        token_hash=RefreshTokenHash(
            model.token_hash
        ),
        expires_at=model.expires_at,
        revoked_at=model.revoked_at,
    )


def refresh_session_to_orm(
    session: RefreshSession,
) -> RefreshTokenOrm:
    return RefreshTokenOrm(
        user_id=session.user_id,
        token_hash=session.token_hash.value,
        expires_at=session.expires_at,
        revoked_at=session.revoked_at,
    )