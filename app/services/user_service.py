from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(user_in: UserCreate, db: Session) -> User:
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already taken")

    hashed_pw = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
