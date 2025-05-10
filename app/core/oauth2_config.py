import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER_CONFIG = {
    "google": {
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    },
    "github": {
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
    },
    "kakao": {
        "token_url": "https://kauth.kakao.com/oauth/token",
        "userinfo_url": "https://kapi.kakao.com/v2/user/me",
        "client_id": os.getenv("KAKAO_CLIENT_ID"),
        "client_secret": os.getenv("KAKAO_CLIENT_SECRET"),
    },
    "naver": {
        "token_url": "https://nid.naver.com/oauth2.0/token",
        "userinfo_url": "https://openapi.naver.com/v1/nid/me",
        "client_id": os.getenv("NAVER_CLIENT_ID"),
        "client_secret": os.getenv("NAVER_CLIENT_SECRET"),
    },
}