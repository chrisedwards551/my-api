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
from app.schemas.errors import ErrorResponse

from app.models.users import User

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


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
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
            detail={
                "error": "invalid_credentials",
                "message": "Invalid email or password",
                "status_code": 401
            }
        )


    # Check if account is temporarily locked
    if (
        user.locked_until
        and user.locked_until > datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=403,
            detail={
                "error": "account_locked",
                "message": "Account temporarily unavailable",
                "status_code": 403
            }
        )


    # Verify password
    if not verify_password(
        user_credentials.password,
        user.password_hash
    ):

        user.failed_login_attempts += 1


        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:

            user.locked_until = (
                datetime.now(timezone.utc)
                + timedelta(minutes=15)
            )

            user.failed_login_attempts = 0


        db.commit()


        raise HTTPException(
            status_code=401,
            detail={
                "error": "invalid_credentials",
                "message": "Invalid email or password",
                "status_code": 401
            }
        )


    # Successful login resets security counters
    user.failed_login_attempts = 0
    user.locked_until = None

    db.commit()


    access_token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }
    )


    refresh_token = create_refresh_token(
        {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
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


@router.post(
    "/refresh",
    response_model=TokenResponse
)
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
    user_role = payload.get("role")


    # Revoke old refresh token
    revoke_refresh_token(
        db,
        request.refresh_token
    )


    # Create new tokens
    new_access_token = create_access_token(
        {
            "sub": user_email,
            "user_id": user_id,
            "role": user_role
        }
    )


    new_refresh_token = create_refresh_token(
        {
            "sub": user_email,
            "user_id": user_id,
            "role": user_role
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


@router.get(
    "/me",
    response_model=UserResponse
)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user