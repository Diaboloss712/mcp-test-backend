from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), unique=True, nullable=False)
    pinecone_id = Column(String, nullable=False)  # 일반적으로 str(problem_id)

    problem = relationship("Problem", back_populates="embedding")