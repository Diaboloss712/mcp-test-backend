from typing import Optional
from fastapi import HTTPException, status
from app.core.security import verify_password, hash_password, create_access_token
from app.core.oauth2_config import PROVIDER_CONFIG
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserSocialCreate
from app.crud.user import (
    get_user_by_email_and_provider,
    get_user_by_username,
    get_user_by_email,
    create_user,
    update_user_fields
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx


async def login_service(form_data, db: AsyncSession):
    user = await authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token({"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}


async def social_login_service(payload: UserSocialCreate, db: AsyncSession):
    config = PROVIDER_CONFIG.get(payload.provider)
    if not config:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    token_json = await _fetch_token(config, payload.code, payload.provider)
    access_token = token_json.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="access_token 없음")

    userinfo = await _fetch_userinfo(config["userinfo_url"], access_token)
    email = extract_email(payload.provider, userinfo)
    if not email:
        raise HTTPException(status_code=400, detail="이메일 없음")

    user = await get_user_by_email_and_provider(db, email, payload.provider)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "User not registered",
                "email": email,
                "provider": payload.provider
            }
        )

    return {"access_token": create_access_token({"sub": user.id, "username": user.username})}


async def register_user_service(register_user: UserCreate, db: AsyncSession) -> User:
    if await get_user_by_username(db, register_user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if await get_user_by_email(db, register_user.email):
        raise HTTPException(status_code=400, detail="Email already taken")

    user = _build_user_model(
        email=register_user.email,
        username=register_user.username,
        password=hash_password(register_user.password)
    )
    return await create_user(user, db)


async def register_user_from_social_info(register_user: UserSocialCreate, db: AsyncSession) -> User:
    if await get_user_by_email(db, register_user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = _build_user_model(
        email=register_user.email,
        username=register_user.username,
        provider=register_user.provider,
        password=""
    )
    return await create_user(user, db)


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return user


async def update_profile_service(update_data: UserUpdate, user: User, db: AsyncSession):
    fields = update_data.model_dump(exclude_unset=True)
    return await update_user_fields(user, fields, db)


async def get_profile_service(user: User):
    return user


async def _fetch_token(config: dict, code: str, provider: str) -> dict:
    redirect_uri = config["redirect_uri"]

    async with httpx.AsyncClient() as client:
        res = await client.post(
            config["token_url"],
            data={
                "grant_type": "authorization_code",
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "redirect_uri": redirect_uri,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    return res.json()


async def _fetch_userinfo(userinfo_url: str, access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        res = await client.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="사용자 정보 요청 실패")
    return res.json()


def extract_email(provider: str, userinfo: dict) -> Optional[str]:
    if provider == "google":
        return userinfo.get("email")
    if provider == "github":
        return userinfo.get("email") or userinfo.get("login") + "@github.com"
    if provider == "kakao":
        return userinfo.get("kakao_account", {}).get("email")
    if provider == "naver":
        return userinfo.get("response", {}).get("email")
    return None


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
        provider=provider
    )
