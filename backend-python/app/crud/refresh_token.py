from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.refresh_tokens import RefreshToken


def create_refresh_token(
    db: Session,
    user_id: int,
    token: str,
    expires_at: datetime
):
    db_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token(
    db: Session,
    token: str
):
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token
        )
        .first()
    )


def revoke_refresh_token(
    db: Session,
    token: str
):
    db_token = get_refresh_token(
        db,
        token
    )

    if db_token:
        db_token.revoked = True

        db.commit()
        db.refresh(db_token)

    return db_token


def delete_expired_tokens(
    db: Session
):
    now = datetime.now(timezone.utc)

    db.query(RefreshToken).filter(
        RefreshToken.expires_at < now
    ).delete()

    db.commit()