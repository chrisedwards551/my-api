from app.auth.password_validation import validate_password
from app.auth.security import hash_password
from app.models.users import User
from app.schemas.user import UserCreate, UserRoleUpdate, UserUpdate
from sqlalchemy.orm import Session


def create_user(db: Session, user: UserCreate):

    validate_password(user.password)

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="user",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# -------------------------
# Authentication helper
# -------------------------
def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def update_user(
    db: Session,
    user_id: int,
    user: UserUpdate,
):
    db_user = get_user(db, user_id)

    if db_user is None:
        return None

    if user.username is not None:
        db_user.username = user.username

    if user.email is not None:
        db_user.email = user.email

    if user.password is not None:

        validate_password(user.password)

        db_user.password_hash = hash_password(
            user.password
        )

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
    db: Session,
    user_id: int,
):
    db_user = get_user(db, user_id)

    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()

    return db_user


def update_user_role(
    db: Session,
    user_id: int,
    role_update: UserRoleUpdate,
):
    db_user = get_user(db, user_id)

    if db_user is None:
        return None

    db_user.role = role_update.role

    db.commit()
    db.refresh(db_user)

    return db_user


def count_admin_users(db: Session) -> int:
    return (
        db.query(User)
        .filter(User.role == "admin")
        .count()
    )