# app/models/user.py
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.user_problem import UserProblem
from app.models.comment import Comment

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    solved_problems: List["UserProblem"] = relationship(back_populates="user")
    comments: List["Comment"] = relationship(back_populates="user")


    # 아래는 외래키
    # problems: List["Problem"] = Relationship(back_populates="created_by_user")
    # logs: List["UserProblemLog"] = Relationship(back_populates="user")