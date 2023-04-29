from ninja import Schema
from pydantic import EmailStr, Field


class UserIn(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    password1: str = Field(min_length=6)
    password2: str = Field(min_length=6)


class LoginIn(Schema):
    email: EmailStr
    password: str


class Four0FourOut(Schema):
    detail: str


class VerificationEmailIn(Schema):
    email: EmailStr
    code: str


class ForgetPasswordIn(Schema):
    email: EmailStr


class ChangePasswordIn(Schema):
    email: EmailStr
    code: str
    new_password: str


class DeleteIn(Schema):
    email: EmailStr
    password: str


class UserSchema(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr


class TokenSchema(Schema):
    access: str


class VerificationEmailOut(Schema):
    user: UserSchema
    token: TokenSchema


class LoginOut(Schema):
    email: EmailStr
    token: TokenSchema




