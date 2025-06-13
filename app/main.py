from dotenv import load_dotenv
load_dotenv(override=True, encoding="utf-8")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import get_engine
from app.db.base import Base
from app.api.v1 import user, auth, problem, category, embedding
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db.session import init_engine
from sqlalchemy.ext.asyncio import create_async_engine
import os

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")


def init_app():
    engine = create_async_engine(
        os.getenv("DATABASE_URL"),
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
        echo=False,
        future=True,
    )
    init_engine(engine)

init_app()  # 이 줄이 테스트에서는 무시되고, conftest.py에서 override됨

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)

# 라우터 등록
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(embedding.router, prefix="/api/v1/embedding", tags=["Embedding"])

# app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
# app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])

