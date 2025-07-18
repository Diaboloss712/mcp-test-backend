from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    key_hash = Column(String, unique=True, index=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    problems = relationship("ExamProblem", back_populates="exam")

class ExamProblem(Base):
    __tablename__ = "exam_problems"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"))
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"))
    problem_order = Column(Integer)

    exam = relationship("Exam", back_populates="problems")
