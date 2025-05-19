from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
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
    register_user_from_social_info,
    update_profile_service,
    get_profile_service
)
from app.schemas.user import Token, OAuthCode

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_service(form_data, db)

@router.post("/social-login")
async def social_login(payload: OAuthCode = Body(...), db: AsyncSession = Depends(get_db)):
    return await social_login_service(payload, db)

@router.post("/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user_service(user, db)

@router.post("/social-register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,)
async def social_register(user: UserSocialCreate, db: AsyncSession = Depends(get_db)):
    return await register_user_from_social_info(user, db)

@router.patch("/profile/update", response_model=UserRead)
async def update_profile(update: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await update_profile_service(update, current_user, db)

@router.get("/profile", response_model=UserRead)
async def read_profile(current_user: User = Depends(get_current_user)):
    return await get_profile_service(current_user)
