from fastapi import FastAPI
from app.db.session import engine as async_engine
from app.db.base import Base
from app.api.v1 import problem, category, comment, review, user, auth
from starlette.middleware.sessions import SessionMiddleware
from app.api.v1 import problem
from dotenv import load_dotenv
import os

load_dotenv()
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# 라우터 등록
# app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(auth.router, prefix="/api/v1/oauth2", tags=["OAuth2"])
# app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
# app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
# app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
# app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])

app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])

@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
