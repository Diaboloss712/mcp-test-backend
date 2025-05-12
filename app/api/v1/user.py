from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserRead, UserSocialCreate, UserUpdate
)
from app.services.user_service import (
    login_service,
    social_login_service,
    register_user_service,
    create_user_from_social_info,
    update_profile_service,
    get_profile_service
)
from app.schemas.user import Token, OAuthCode

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_service(form_data, db)

@router.post("/social-login")
async def social_login(payload: OAuthCode = Body(...), db: Session = Depends(get_db)):
    return await social_login_service(payload, db)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(user, db)

@router.post("/social-register", response_model=UserRead)
def social_register(user: UserSocialCreate, db: Session = Depends(get_db)):
    return create_user_from_social_info(user, db)

@router.patch("/profile/update", response_model=UserRead)
def update_profile(update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_profile_service(update, current_user, db)

@router.get("/profile", response_model=UserRead)
def read_profile(current_user: User = Depends(get_current_user)):
    return get_profile_service(current_user)