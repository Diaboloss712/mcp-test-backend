# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


    # 아래는 외래키
    # problems: List["Problem"] = Relationship(back_populates="created_by_user")
    # comments: List["Comment"] = Relationship(back_populates="user")
    # logs: List["UserProblemLog"] = Relationship(back_populates="user")