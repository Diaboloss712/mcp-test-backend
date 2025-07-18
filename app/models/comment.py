from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func  # ✅ ForeignKey 추가
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # ✅ 수정된 부분 시작
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ User 모델과 연결될 외래키 추가
    user = relationship("User", back_populates="comments")  # ✅ 일대다 관계 설정 (User.comments와 연결)
    # ✅ 수정된 부분 끝
