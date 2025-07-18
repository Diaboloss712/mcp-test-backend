# app/crud/user.py
from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_email_and_provider(
    db: AsyncSession, email: str, provider: str
):
    result = await db.execute(
        select(User).where(User.email == email, User.provider == provider)
    )
    return result.scalar_one_or_none()

async def create_user(user: User, db: AsyncSession) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_fields(user: User, fields: dict, db: AsyncSession) -> User:
    for k, v in fields.items():
        setattr(user, k, v)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
