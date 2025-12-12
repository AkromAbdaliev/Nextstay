from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenFormatException,
    TokenExpiredException,
    UnauthorizedException,
    UserNotFoundException,
)
from app.users.service import UsersService


def get_token(reuquest: Request):
    access_token = reuquest.cookies.get("access_token")
    if not access_token:
        raise UnauthorizedException
    return reuquest.cookies.get("access_token")


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise InvalidTokenFormatException
    user_id: str = payload.get("sub")
    if user_id is None:
        raise InvalidTokenFormatException
    email: str = payload.get("email")
    if email is None:
        raise InvalidTokenFormatException
    expire: int = payload.get("exp")
    if expire is None or expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException

    user = await UsersService.find_one_or_none(id=int(user_id))
    if user is None:
        raise UserNotFoundException
    return user
