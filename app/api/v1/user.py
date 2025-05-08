from fastapi import APIRouter, Depends, status
from sqlmodel import Session, SQLModel
from app.schemas.user import UserCreate, UserRead, UserSocialCreate
from app.services.user_service import create_user, create_user_from_social_info
from app.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import authenticate_user
from app.core.security import get_current_user, create_access_token
from starlette.requests import Request


router = APIRouter()

class Token(SQLModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(register_user: UserCreate, db: Session = Depends(get_db)):
    return create_user(register_user, db)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token({
        "sub": str(user.id),
        "username": user.username
    })
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user/profile", response_model=UserRead)
def read_user_profile(current_user: UserRead = Depends(get_current_user)):
    return current_user

@router.post("/social-register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def social_register(
    register_user: UserSocialCreate, db: Session = Depends(get_db)
) -> UserRead:
    return create_user_from_social_info(register_user, db)
