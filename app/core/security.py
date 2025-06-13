from email.message import EmailMessage
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_db
from sqlmodel import select
from app.models.user import User
import aiosmtplib

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
FORGET_PWD_SECRET_KEY = os.getenv("FORGET_PWD_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 120
RESET_TOKEN_EXPIRE_MINUTES = 10

HOSTNAME=os.getenv("SMTP_HOST")
PORT=os.getenv("SMTP_PORT")
USERNAME=os.getenv("SMTP_USER")
PASSWORD=os.getenv("SMTP_PASSWORD")
EMAIL_SENDER=os.getenv("EMAIL_SENDER")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_reset_password_token(email: str):
    expires_delta = timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": datetime.now(timezone.utc) + expires_delta}
    token = jwt.encode(data, FORGET_PWD_SECRET_KEY, ALGORITHM)
    return token

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id") or payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if user is None:
        raise credentials_exception
    return user

async def send_email(to_email: str, link: str):
    subject = "비밀번호 재설정 안내"
    content = f"""
    안녕하세요,<br><br>
    아래 링크를 클릭하여 비밀번호를 재설정하세요:<br>
    <a href="{link}">{link}</a><br><br>
    이 링크는 10분 동안만 유효합니다.
    """

    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=HOSTNAME,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        start_tls=True,
    )