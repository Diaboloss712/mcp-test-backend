from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserSocialCreate(UserBase):
    provider: Literal["google", "kakao", "naver", "github"]

class UserRead(UserBase):
    id: int
    is_admin: bool
    provider: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델 → Pydantic 변환 시 필요

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class OAuthCode(BaseModel):
    provider: str
    code: str
