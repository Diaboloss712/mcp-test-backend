from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None

def init_engine(engine: AsyncEngine):
    global _engine, _session_factory
    _engine = engine
    _session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_engine():
    if _engine is None:
        raise RuntimeError("Engine is not initialized")
    return _engine

def get_session_factory():
    if _session_factory is None:
        raise RuntimeError("SessionFactory is not initialized")
    return _session_factory

async def get_db():
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session