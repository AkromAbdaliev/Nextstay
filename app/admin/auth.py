from typing import Optional

from fastapi import status
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.users.service import UsersService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        # Validate user with your existing authentication
        user = await UsersService.find_one_or_none(email=email)
        if not user:
            return False

        from app.users.auth import verify_password  # your function

        if not verify_password(password, user.hashed_password):
            return False

        # Save a session key SQLAdmin will use
        # You can store user id or email, SQLAdmin just needs it truthy
        request.session["user"] = {"id": user.id, "email": user.email}
        return True

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        """
        SQLAdmin calls this for EVERY request.
        Must return:
        - True/False → allowed / redirect
        - Response → custom redirect
        """
        user_session = request.session.get("user")
        if not user_session:
            return RedirectResponse(
                url="/admin/login", status_code=status.HTTP_302_FOUND
            )

        # Optional: verify user still exists in DB
        user = await UsersService.find_one_or_none(id=user_session.get("id"))
        if not user:
            # session is invalid
            request.session.clear()
            return RedirectResponse(
                url="/admin/login", status_code=status.HTTP_302_FOUND
            )

        # everything ok
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
