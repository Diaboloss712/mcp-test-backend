from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, SQLModel, select
from app.schemas.user import UserCreate, UserRead, UserSocialCreate
from app.services.user_service import create_user
from app.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import authenticate_user
from app.core.security import get_current_user, create_access_token
from app.models.user import User
from app.core.oauth2_config import PROVIDER_CONFIG
import httpx

router = APIRouter()

class Token(SQLModel):
    access_token: str
    token_type: str

class OAuthCode(SQLModel):
    provider: str
    code: str

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

@router.post("/social-register", response_model=UserRead)
async def social_register(
    register_user: UserSocialCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.exec(
        select(User).where(User.email == register_user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 사용자입니다.")

    user = User(
        email=register_user.email,
        username=register_user.username,
        provider=register_user.provider,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/social-login")
async def social_login(payload: OAuthCode = Body(...), db: Session = Depends(get_db)):
    config = PROVIDER_CONFIG.get(payload.provider)
    if not config:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    # access_token 요청
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            config["token_url"],
            data={
                "grant_type": "authorization_code",
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "redirect_uri": f"http://localhost:5173/callback?provider={payload.provider}",
                "code": payload.code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        print("token_res.status_code:", token_res.status_code)
        print("token_res.text:", token_res.text)

    if token_res.status_code != 200:
        raise HTTPException(status_code=400, detail="토큰 요청 실패")

    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="access_token 없음")

    async with httpx.AsyncClient() as client:
        userinfo_res = await client.get(
            config["userinfo_url"],
            headers={"Authorization": f"Bearer {access_token}"}
        )

    userinfo = userinfo_res.json()

    email = extract_email(payload.provider, userinfo)

    if not email:
        raise HTTPException(status_code=400, detail="이메일 없음")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "User not registered",
                "email": email,
                "provider": payload.provider
            }
    )

    return {"access_token": create_access_token(user.email)}


def extract_email(provider: str, userinfo: dict) -> str | None:
    if provider == "google":
        return userinfo.get("email")
    elif provider == "github":
        return userinfo.get("email") or userinfo.get("login") + "@github.com"
    elif provider == "kakao":
        return userinfo.get("kakao_account", {}).get("email")
    elif provider == "naver":
        return userinfo.get("response", {}).get("email")
    return None