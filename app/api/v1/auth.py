import os
from fastapi import APIRouter, Body, Depends, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2PasswordRequestForm
from starlette.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.oauth2_providers import PROVIDER_CONFIGS
from app.core.security import ALGORITHM, create_reset_password_token, hash_password, send_email
from app.crud.user import get_user_by_email, update_user_fields
from app.db.session import get_db
from jose import JWTError, jwt

from app.schemas.user import OAuthCode
from app.schemas.user import (
    UserCreate, UserRead, UserSocialCreate
)
from app.services.auth_service import (
    login_service,
    social_login_service,
    register_user_service,
    register_user_from_social_info
)
from app.schemas.user import Token, OAuthCode
FORGET_PWD_SECRET_KEY = os.getenv("FORGET_PWD_SECRET_KEY")

router = APIRouter()

config = Config(".env")
oauth = OAuth(config)
for provider_name, provider_conf in PROVIDER_CONFIGS.items():
    oauth.register(
        name=provider_name,
        client_id=os.getenv(f"{provider_name.upper()}_CLIENT_ID"),
        client_secret=os.getenv(f"{provider_name.upper()}_CLIENT_SECRET"),
        **provider_conf
    )

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

@router.post("/forgot-password", name="forgot-password")
async def forgot_password(
    email: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        token = create_reset_password_token(email)
        reset_link = f"https://yourdomain.com/reset-password?token={token}"
        await send_email(email, reset_link)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"msg": "Reset link sent"}

@router.post("/reset-password", name="reset-password")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, FORGET_PWD_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await update_user_fields(user, {"password": hash_password(new_password)}, db)
    return {"msg": "Password has been reset"}
