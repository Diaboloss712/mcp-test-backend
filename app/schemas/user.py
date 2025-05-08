from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, Literal


class UserBase(SQLModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserSocialCreate(UserBase):
    password: Optional[str] = None
    provider: Literal["google", "kakao", "naver", "github"]

class UserRead(UserBase):
    id: int
    is_admin: bool
    created_at: datetime