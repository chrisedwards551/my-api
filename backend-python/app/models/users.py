from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )


    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )


    password_hash: Mapped[str] = mapped_column(
        String
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )