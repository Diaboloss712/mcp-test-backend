from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserSocialCreate
from app.core.security import hash_password
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.core.security import verify_password
from datetime import datetime, timezone


def get_user_by_username(db: Session, username: str) -> User:
    return db.exec(select(User).where(User.username == username)).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.exec(select(User).where(User.email == email)).first()


def create_user( register_user: UserCreate, db: Session) -> User:
    if get_user_by_username(db,  register_user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(db,  register_user.email):
        raise HTTPException(status_code=400, detail="Email already taken")

    user = _build_user_model(
        email= register_user.email,
        username= register_user.username,
        password=hash_password( register_user.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return user

def get_user_from_social_or_fail(
    user_info: dict,
    provider: str,
    db: Session
) -> User:
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"No account linked to {provider}")

    return user

def create_user_from_social_info(register_user: UserSocialCreate, db: Session) -> User:
    if get_user_by_email(db, register_user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = _build_user_model(
        email= register_user.email,
        username= register_user.username,
        provider= register_user.provider,
        password=""
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def _build_user_model(
    email: str,
    username: str,
    password: Optional[str] = "",
    is_admin: bool = False,
    provider: Optional[str] = None
) -> User:
    return User(
        username=username,
        email=email,
        password=password or "",
        is_admin=is_admin,
        provider = provider
    )
