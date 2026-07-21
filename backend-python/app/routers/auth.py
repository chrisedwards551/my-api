from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.crud.user import get_user_by_email
from app.crud.refresh_token import (
    create_refresh_token as save_refresh_token,
    get_refresh_token,
    revoke_refresh_token
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshRequest
)

from app.schemas.user import UserResponse

from app.auth.security import verify_password

from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    user_credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    user = get_user_by_email(
        db,
        user_credentials.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not verify_password(
        user_credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    access_token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id
        }
    )


    refresh_token = create_refresh_token(
        {
            "sub": user.email,
            "user_id": user.id
        }
    )


    save_refresh_token(
        db,
        user.id,
        refresh_token,
        datetime.now(timezone.utc) + timedelta(days=7)
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):

    stored_token = get_refresh_token(
        db,
        request.refresh_token
    )


    if not stored_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )


    if stored_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked"
        )


    payload = decode_token(
        request.refresh_token
    )


    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Expired refresh token"
        )


    user_email = payload.get("sub")
    user_id = payload.get("user_id")


    revoke_refresh_token(
        db,
        request.refresh_token
    )


    new_access_token = create_access_token(
        {
            "sub": user_email,
            "user_id": user_id
        }
    )


    new_refresh_token = create_refresh_token(
        {
            "sub": user_email,
            "user_id": user_id
        }
    )


    save_refresh_token(
        db,
        user_id,
        new_refresh_token,
        datetime.now(timezone.utc) + timedelta(days=7)
    )


    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user = Depends(get_current_user)
):
    return current_user