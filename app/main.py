from fastapi import FastAPI
from app.api.v1 import problem
from app.db.session import engine as async_engine
from app.db.base import Base
from app.api.v1 import user, category, comment, review
from app.api.v1 import problem as problem_router
from app.models import category, problem


app = FastAPI()

# app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
# app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
# app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
# app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])

@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 라우터 등록
app.include_router(problem_router.router, prefix="/api/v1/problems", tags=["Problems"])
