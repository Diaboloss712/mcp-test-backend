from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), unique=True, nullable=False)
    # vector = Column(Vector(1024), nullable=False) 앞으로 pgvector가 아닌 pinecone에서 vectorDB 담당

    problem = relationship("Problem", back_populates="embedding")
