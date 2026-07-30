from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.users import User

from app.crud.permission import has_permission


# Existing RBAC check
def require_role(required_role: str):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker


# Phase 15.8 Permission-Based Authorization

def require_permission(permission_name: str):

    def permission_checker(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):

        allowed = has_permission(
            db,
            current_user.role,
            permission_name
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return permission_checker