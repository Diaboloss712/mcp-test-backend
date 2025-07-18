from typing import TYPE_CHECKING, List  # ✅ List 추가
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.comment import Comment  # ✅ Comment 클래스 타입 힌트용 import
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

    solved_problems: Mapped[List["UserProblem"]] = relationship(back_populates="user")

    # ✅ 'comments' 관계 정의 유지 (Comment 클래스가 존재해야 함)
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")


    # 아래는 외래키
    # problems: List["Problem"] = Relationship(back_populates="created_by_user")
    # logs: List["UserProblemLog"] = Relationship(back_populates="user")