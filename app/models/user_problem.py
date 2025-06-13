from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserProblem(Base):
    __tablename__ = "user_problems"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    solved_at = Column(DateTime, server_default=func.now())
    is_correct = Column(Boolean, default=False)
    attempt_number = Column(Integer, default=1)

    user = relationship("User", back_populates="solved_problems")
    problem = relationship("Problem", back_populates="solved_users")
