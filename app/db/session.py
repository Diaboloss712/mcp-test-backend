# app/db/session.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL")

# 1) SQLAlchemy 비동기 엔진에 poolclass=NullPool 추가
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,   # ← 여기를 추가
)

# 2) SQLModel AsyncSession
SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with SessionFactory() as session:
        yield session
