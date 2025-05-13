from sqlmodel import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # 부모 카테고리와 자식 카테고리 연결
    parent = relationship("Category", remote_side=[id], backref="children")
