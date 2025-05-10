from fastapi import FastAPI
from app.api.v1 import problem, category, comment, review, user, auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

app = FastAPI()

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

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/oauth2", tags=["OAuth2"])
# app.include_router(problem.router, prefix="/api/v1/problems", tags=["Problems"])
# app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
# app.include_router(comment.router, prefix="/api/v1/comments", tags=["Comments"])
# app.include_router(review.router, prefix="/api/v1/review", tags=["Review"])