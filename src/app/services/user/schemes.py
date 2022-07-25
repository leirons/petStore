from typing import Optional, Union

from pydantic import (
    BaseModel,
    ValidationError,
    validator
)

from app.services.user.validate import validate_email


class UserBase(BaseModel):
    email: str = "string@gmail.com"
    first_name:str = "Ivan"
    last_name:str = "Grechka"
    phone:str = "380502906561"

    @validator("email")
    def validate_email(cls, email):
        if validate_email(email):
            return email
        raise ValidationError("Email does not correct")


class UserCreate(UserBase):
    password: str
    login: str

    @validator("login")
    def validate_login(cls, login):
        if len(login) > 30:
            return ValidationError("Login should not have more than 30 symbols ")
        return login


class User(UserBase):
    id: int
    login: str
    password: str

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    login: Optional[Union[str, None]] = None
    password: Optional[Union[str, None]] = None
