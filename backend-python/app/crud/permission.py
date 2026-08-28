from app.models.permissions import Permission, RolePermission
from sqlalchemy.orm import Session

# -------------------------
# Permission CRUD
# -------------------------

def create_permission(
    db: Session,
    name: str,
    description: str | None = None
):
    permission = Permission(
        name=name,
        description=description
    )

    db.add(permission)
    db.commit()
    db.refresh(permission)

    return permission


def get_permissions(
    db: Session
):
    return (
        db.query(Permission)
        .all()
    )


def get_permission(
    db: Session,
    permission_id: int
):
    return (
        db.query(Permission)
        .filter(
            Permission.id == permission_id
        )
        .first()
    )


def get_permission_by_name(
    db: Session,
    name: str
):
    return (
        db.query(Permission)
        .filter(
            Permission.name == name
        )
        .first()
    )


# -------------------------
# Role Permission CRUD
# -------------------------

def assign_permission_to_role(
    db: Session,
    role: str,
    permission_id: int
):

    role_permission = RolePermission(
        role=role,
        permission_id=permission_id
    )

    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)

    return role_permission


def get_role_permissions(
    db: Session,
    role: str
):

    return (
        db.query(RolePermission)
        .filter(
            RolePermission.role == role
        )
        .all()
    )


def remove_permission_from_role(
    db: Session,
    role: str,
    permission_id: int
):

    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role == role,
            RolePermission.permission_id == permission_id
        )
        .first()
    )

    if role_permission:

        db.delete(role_permission)
        db.commit()

    return role_permission


# -------------------------
# Permission Verification
# -------------------------

def has_permission(
    db: Session,
    role: str,
    permission_name: str
):

    permission = (
        db.query(Permission)
        .filter(
            Permission.name == permission_name
        )
        .first()
    )

    if permission is None:
        return False


    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role == role,
            RolePermission.permission_id == permission.id
        )
        .first()
    )

    return role_permission is not None