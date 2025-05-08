# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/mcp_test"
#postgresql+asyncpg://iinje@localhost/mcp_db   for Mac 

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

# FastAPI dependency
async def get_db():
    async with async_session() as session:
        yield session
