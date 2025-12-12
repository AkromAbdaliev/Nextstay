from pydantic import BaseModel, ConfigDict, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class SUserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class SUserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    model_config = ConfigDict(from_attributes=True)
