from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_in, db)