from fastapi import FastAPI

from app.api.v1 import user, problem, category, comment, review

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])
