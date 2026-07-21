from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.user import get_user_by_email
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse

from app.auth.security import verify_password
from app.auth.jwt import create_access_token
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


    token = create_access_token(
    {
        "sub": user.email,
        "user_id": user.id
    }
)


    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user = Depends(get_current_user)
):
    return current_user