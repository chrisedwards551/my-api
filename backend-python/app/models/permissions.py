from app.database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
        nullable=False
    )

    permission: Mapped["Permission"] = relationship()