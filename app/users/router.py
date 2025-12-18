from fastapi import APIRouter, Depends, Response, status

from app.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_user
from app.users.schemas import SUserRead, SUserRegister, SUserUpdate
from app.users.service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=SUserRead)
async def register_user(user_data: SUserRegister):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    return await UsersService.add_one(
        email=user_data.email, hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(user_data: SUserRegister, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidCredentialsException
    access_token = create_access_token(
        data={"sub": str(user.id), "email": str(user.email)}
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/me", response_model=SUserRead)
async def get_me(current_user: SUserRead = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=list[SUserRead])
async def get_users():
    return await UsersService.find_all()


@router.get("/users/{user_id}", response_model=SUserRead)
async def get_user(user_id: int):
    user = await UsersService.find_one_or_none(id=user_id)
    if not user:
        raise UserNotFoundException

    return user


@router.post("/users", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: SUserRegister):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersService.add_one(
        email=user_data.email, hashed_password=hashed_password
    )

    return SUserRead.model_validate(new_user)


@router.put(
    "/users/{user_id}", response_model=SUserRead, status_code=status.HTTP_202_ACCEPTED
)
async def update_user(user_id: int, user_data: SUserUpdate):
    user = await UsersService.find_by_id(user_id)
    if not user:
        raise UserNotFoundException

    update_fields = {}
    if user_data.email is not None:
        update_fields["email"] = user_data.email
    if user_data.password is not None:
        update_fields["hashed_password"] = get_password_hash(user_data.password)

    return await UsersService.update_one(user, **update_fields)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user = await UsersService.find_by_id(user_id)
    if not user:
        raise UserNotFoundException
    return await UsersService.delete_one(user)
