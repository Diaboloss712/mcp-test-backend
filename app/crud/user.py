from sqlmodel import Session, select
from app.models.user import User

def get_user_by_username(db: Session, username: str) -> User:
    return db.exec(select(User).where(User.username == username)).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.exec(select(User).where(User.email == email)).first()

def create_user(user: User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_fields(user: User, fields: dict, db: Session):
    for key, value in fields.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user