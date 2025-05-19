# app/crud/user.py
from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    q = select(User).where(User.username == username)
    result = await db.exec(q)
    return result.first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = select(User).where(User.email == email)
    result = await db.exec(q)
    return result.first()


async def create_user(user: User, db: AsyncSession) -> User:
    db.add(user)
    await db.flush()
    await db.commit()
    return user


async def update_user_fields(user: User, fields: dict, db: AsyncSession) -> User:
    for k, v in fields.items():
        setattr(user, k, v)
    db.add(user)
    await db.flush()
    await db.commit()
    return user
