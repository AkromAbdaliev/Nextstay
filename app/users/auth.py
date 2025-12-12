from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.config import settings
from app.users.service import UsersService

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode["exp"] = int(expire.timestamp())
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersService.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
