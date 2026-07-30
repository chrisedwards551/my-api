from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_permission

from app.crud.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    update_user_role,
    count_admin_users,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserRoleUpdate,
)

from app.models.users import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


# -----------------------------------
# Phase 15.8 Permission Authorization
# users.read permission required
# -----------------------------------

@router.get("/", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("users.read")
    )
):

    return get_users(db)


# -----------------------------------
# View single user
# User can view themselves
# Admin can view anyone
# -----------------------------------

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if (
        current_user.id != user_id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this user."
        )

    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# -----------------------------------
# Update user information
# -----------------------------------

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("users.update")
    )
):
    
    if (
        current_user.id != user_id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this user."
        )

    updated_user = update_user(
        db,
        user_id,
        user
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user


# -----------------------------------
# Phase 15.7 Role Management
# -----------------------------------

@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role_endpoint(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("users.manage_roles")
    )
):


    target_user = get_user(
        db,
        user_id
    )


    if target_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )


    # Prevent removing your own admin access
    if (
        current_user.id == user_id
        and role_update.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot remove your own admin privileges."
        )


    # Prevent deleting the last admin
    if (
        target_user.role == "admin"
        and role_update.role != "admin"
        and count_admin_users(db) <= 1
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot remove the last admin account."
        )


    return update_user_role(
        db,
        user_id,
        role_update
    )



# -----------------------------------
# Delete user
# -----------------------------------

@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("users.delete")
    )
):

    if (
        current_user.id != user_id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
        )


    deleted_user = delete_user(
        db,
        user_id
    )


    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )


    return deleted_user