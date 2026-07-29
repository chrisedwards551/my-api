from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user

from app.models.users import User

from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    RolePermissionCreate,
    RolePermissionResponse
)

from app.crud.permission import (
    create_permission,
    get_permissions,
    assign_permission_to_role,
    remove_permission_from_role
)


router = APIRouter(
    prefix="/permissions",
    tags=["permissions"]
)


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )

    return current_user


@router.post(
    "/",
    response_model=PermissionResponse
)
def create_new_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return create_permission(
        db,
        permission.name,
        permission.description
    )


@router.get(
    "/",
    response_model=list[PermissionResponse]
)
def read_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return get_permissions(db)


@router.post(
    "/assign",
    response_model=RolePermissionResponse
)
def assign_role_permission(
    data: RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return assign_permission_to_role(
        db,
        data.role,
        data.permission_id
    )


@router.delete(
    "/remove",
    response_model=RolePermissionResponse
)
def remove_role_permission(
    data: RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    removed = remove_permission_from_role(
        db,
        data.role,
        data.permission_id
    )

    if removed is None:
        raise HTTPException(
            status_code=404,
            detail="Permission assignment not found."
        )

    return removed