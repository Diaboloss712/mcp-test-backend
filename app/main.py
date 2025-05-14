from dotenv import load_dotenv
load_dotenv(override=True, encoding="utf-8")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine as async_engine
from app.db.base import Base
from app.api.v1 import user, auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    await async_engine.dispose()


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
app.include_router(auth.router, prefix="/api/v1/oauth2", tags=["OAuth2"])
# app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
# app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
# app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
# app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])

# app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])

