import os
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.pool import NullPool

from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app
from app.db.session import get_db

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(autouse=True, scope="function")
async def clean_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

@pytest.fixture(scope="function")
def override_get_db():
    async def _override():
        async with SessionFactory() as session:
            yield session
    return _override

@pytest.fixture(scope="function")
async def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
async def db_session():
    async with SessionFactory() as session:
        yield session