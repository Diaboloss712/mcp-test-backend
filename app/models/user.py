from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.user_problem import UserProblem

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    provider: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # 관계 설정 (SQLAlchemy 2.0)
    solved_problems: Mapped[list["UserProblem"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    # 아래는 외래키
    # problems: List["Problem"] = Relationship(back_populates="created_by_user")
    # logs: List["UserProblemLog"] = Relationship(back_populates="user")