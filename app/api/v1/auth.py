from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request
from fastapi import APIRouter, Depends
from app.core.oauth2_providers import PROVIDER_CONFIGS
from app.services.user_service import get_user_from_social_or_fail
from app.api.v1.user import create_access_token
from sqlmodel import Session
from app.db.session import get_db
import os

router = APIRouter()
config = Config(".env")
oauth = OAuth(config)

for name, conf in PROVIDER_CONFIGS.items():
    oauth.register(
        name=name,
        client_id=os.getenv(f"{name.upper()}_CLIENT_ID"),
        client_secret=os.getenv(f"{name.upper()}_CLIENT_SECRET"),
        **conf
    )

@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    redirect_uri = request.url_for("auth", provider=provider)
    client = oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/auth/{provider}")
async def auth(request: Request, provider: str, db: Session = Depends(get_db)):
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    if provider == "google":
        user_info = await client.parse_id_token(request, token)
    else:
        user_info = token.get("userinfo") or await client.userinfo()
    user = get_user_from_social_or_fail(user_info, provider, db)

    jwt = create_access_token({"sub": str(user.id), "provider": provider, "email": user.email})
    return {"access_token": jwt, "token_type": "bearer"}
