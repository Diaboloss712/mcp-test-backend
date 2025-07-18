from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import Mapped, relationship
from app.db.base import Base
import enum

from app.models.user_problem import UserProblem


class ProblemType(str, enum.Enum):
    select = "select"
    write = "write"

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(SqlEnum(ProblemType), nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    embedding = relationship("Embedding", back_populates="problem", uselist=False, cascade="all, delete-orphan")
    
    user_problem_records: Mapped[List["UserProblem"]] = relationship(
        back_populates="problem", cascade="all, delete-orphan"
    )
    # solved_users: Mapped[List["User"]] = relationship(back_populates="solved_problems")
