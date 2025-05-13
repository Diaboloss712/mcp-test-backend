import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.oauth2_providers import PROVIDER_CONFIGS
from app.core.security import create_access_token
from app.crud.user import get_user_by_email
from app.db.session import get_db

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
