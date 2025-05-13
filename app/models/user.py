from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"  # 선택사항 (자동 설정됨)

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, nullable=False, unique=True)
    email: str = Field(max_length=100, nullable=False, unique=True)
    password: Optional[str] = Field(default=None, nullable=True)
    is_admin: bool = Field(default=False)
    provider: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # 아래는 외래키
    # problems: List["Problem"] = Relationship(back_populates="created_by_user")
    # comments: List["Comment"] = Relationship(back_populates="user")
    # logs: List["UserProblemLog"] = Relationship(back_populates="user")