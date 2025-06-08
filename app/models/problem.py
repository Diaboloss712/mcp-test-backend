from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class ProblemType(str, enum.Enum):
    select = "select"
    write = "write"

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(SqlEnum(ProblemType), nullable=False)
    answer = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    embedding = relationship("Embedding", back_populates="problem", uselist=False, cascade="all, delete-orphan")
