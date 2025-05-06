from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
