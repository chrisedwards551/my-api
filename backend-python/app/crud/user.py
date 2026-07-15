from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import hash_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        if user_data.username:
            db_user.username = user_data.username

        if user_data.email:
            db_user.email = user_data.email

        if user_data.password:
            db_user.password_hash = hash_password(user_data.password)

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user