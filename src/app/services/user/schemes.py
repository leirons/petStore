from typing import Optional, Union

from pydantic import BaseModel, validator

from app.services.user.validate import validate_email


class UserBase(BaseModel):
    email: str = "string@gmail.com"
    first_name: str = "Ivan"
    last_name: str = "Grechka"
    phone: str = "380502906561"

    @validator("email")
    def validate_email(cls, email):
        if validate_email(email):
            return email
        raise ValueError("Email does not correct")


class UserCreate(UserBase):
    password: str = "string355"
    username: str = "string355"

    @validator("username")
    def validate_login(cls, username):
        if len(username) > 30:
            raise ValueError("Username should not have more than 30 symbols ")
        elif len(username) < 8:
            raise ValueError("Username should have more than 8 symbols ")
        return username

    @validator("password")
    def validate_password(cls, password):
        if len(password) > 30:
            raise ValueError("Password should not have more than 30 symbols ")
        elif len(password) < 8:
            raise ValueError("Password should have more than 8 symbols ")
        return password


class User(UserBase):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    username: str = "string355"
    password: str = "string355"

    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    username: Optional[Union[str, None]] = "string355"
    password: Optional[Union[str, None]] = "string355"
