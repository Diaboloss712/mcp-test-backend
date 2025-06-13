import os
import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from asgi_lifespan import LifespanManager
from app.db.base import Base
import app.db.session as session_module

from app.main import app
from app.db.session import get_db as app_get_db, init_engine

DATABASE_URL = os.getenv("DATABASE_TEST_URL")

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def engine():
    test_engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        future=True,
    )
    yield test_engine
    await test_engine.dispose()

@pytest.fixture(scope="function", autouse=True)
async def override_engine(engine):
    init_engine(engine)

@pytest.fixture(scope="function")
async def session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="function")
async def clean_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
async def db_session(clean_db, session_factory):
    async with session_factory() as session:
        yield session

@pytest.fixture(scope="function")
async def client(clean_db, session_factory):
    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[app_get_db] = override_get_db

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()
