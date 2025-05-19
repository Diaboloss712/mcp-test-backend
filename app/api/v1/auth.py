import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.oauth2_providers import PROVIDER_CONFIGS
from app.core.security import ALGORITHM, create_access_token, create_reset_password_token, hash_password, send_email
from app.crud.user import get_user_by_email
from app.db.session import get_db
from jose import JWTError, jwt

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

@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    client = getattr(oauth, provider)
    redirect_uri = request.url_for("auth", provider=provider)
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/auth/{provider}", name="auth")
async def auth(
    request: Request,
    provider: str,
    db: AsyncSession = Depends(get_db),
):
    client = getattr(oauth, provider)
    token = await client.authorize_access_token(request)

    if provider.lower() == "google":
        user_info = await client.parse_id_token(request, token)
    else:
        user_info = token.get("userinfo") or await client.userinfo(request, token=token)

    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email not provided by provider")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not registered")

    access_token = create_access_token({
        "user_id": str(user.id),
        "provider": provider,
        "email": user.email
    })
    return {"access_token": access_token, "token_type": "bearer"}

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
    except Exception as err:
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

    user.hashed_password = hash_password(new_password)
    db.add(user)
    await db.commit()
    return {"msg": "Password has been reset"}